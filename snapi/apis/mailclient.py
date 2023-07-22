# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-07-17 18:46:50
# @Last Modified by:   chunyang.xu
# @Last Modified time: 2023-07-22 21:12:24


import os
import json

from .base import SnBaseApi
from snapi.conf import UpdateApi

import logging
maillogger = logging.getLogger(__name__)


class MailClient(SnBaseApi):

    def __init__(self, ip_address: str, port: str, username: str, password: str, otp_code: str = None):
        self.app = 'MailClient'
        super(MailClient, self).__init__(self.app, ip_address, port, username, password, otp_code)
        self.update_mailbox_api = UpdateApi()
        self.mailboxfile = os.path.join(os.getcwd(), 'snapi/conf/mailbox/mailbox.json')

    def get_mailboxes_api(self):
        api_name = 'SYNO.MailClient.Mailbox'
        params = {'method': 'list', 'conversation_view': 'false', 'subscription': 'false', 
                  'additional': ["unread_count", "draft_total_count"]}
        snres_json = self.snapi_requests(api_name, params, method='post')
        mailboxes = snres_json.get('data').get('mailbox')
        self.update_mailbox_api.dump(self.mailboxfile, mailboxes)
        return mailboxes

    def get_mailboxes(self):
        mailboxes = self.update_mailbox_api.load(self.mailboxfile)
        if not mailboxes:
            mailboxes = self.get_mailboxes_api()

        return mailboxes

    def get_mailbox_info(self, mailbox_name: str = None, mailbox_id: int = None):
        mailboxes = self.get_mailboxes()

        for mailbox in mailboxes:
            _mailbox_name, _mailbox_id = mailbox.get('path'), mailbox.get('id')
            if _mailbox_name == mailbox_name:
                break
            if _mailbox_id == mailbox_id:
                break
        else:
            mailboxes_all = [(mbox.get('id'), mbox.get('path')) for mbox in mailboxes]
            nonexist = f"[mailbox_name]::{mailbox_name}" if mailbox_name else f"[mailbox_id]::{mailbox_id}"
            raise ValueError(f"Only find {mailboxes_all}, {nonexist} not exist !!! ")

        return mailbox

    def get_maillabels_api(self):
        api_name = 'SYNO.MailClient.Label'
        params = {'method': 'list', 'conversation_view': 'false', 'additional': ["unread_count"]}
        snres_json = self.snapi_requests(api_name, params, method='post')
        return snres_json

    def get_filters(self):
        api_name = 'SYNO.MailClient.Filter'
        params = {'method': 'list'}
        snres_json = self.snapi_requests(api_name, params, method='post')
        filters = snres_json.get('data').get('filter')
        return filters

    def filter_act(self, condition: dict, action: dict, idx: int):
        api_name = 'SYNO.MailClient.Filter'
        condition = self.convert_to_json(condition)
        action = self.convert_to_json(action)
        params = {'method': 'set', 'condition': condition, 'action': action, 'id': idx, 
                  'conversation_view': 'false', 'apply_exist': 'true'}
        snres_json = self.snapi_requests(api_name, params, method='post')
        return snres_json

    def filter(self):
        results = {}
        filters = self.get_filters()
        for f in filters:
            enabled, condition, action, idx = f.get('enabled'), f.get('condition'), f.get('action'), f.get('id')

            # if idx != 15:
            #     continue

            if enabled:
                snres_json = self.filter_act(condition, action, idx)
                results[idx] = {'result': snres_json, 'condition': condition, 'action': action}
        return results

    def get_mails(self, mailbox_id: int = -1, offset: int = 0, limit: int = 200):
        ids = []
        mails = []
        api_name = 'SYNO.MailClient.Thread'
        condition = [{"name": "mailbox", "value": f"{mailbox_id}"}]
        condition = self.convert_to_json(condition)
        params = {'method': 'list', 'offset': f'{offset}', 'limit': f'{limit}', 'condition': condition, 
                  'conversation_view': 'false'}
        snres_json = self.snapi_requests(api_name, params, method='post')
        _mails = snres_json.get('data').get('thread')
        _ids = snres_json.get('data').get('matched_ids')
        while _mails:
            mails.extend(_mails)
            ids.extend(_ids)
            offset += limit
            params['offset'] = offset
            snres_json = self.snapi_requests(api_name, params, method='post')
            _mails = snres_json.get('data').get('thread')
            _ids = snres_json.get('data').get('matched_ids')

        counts = len(mails)
        mailbox = self.get_mailbox_info(mailbox_id=mailbox_id)
        mailbox_name = mailbox.get('path')
        maillogger.info(f"[{mailbox_name}]has email {counts} counts ! ")
        return ids, mails

    def spam_report(self):
        api_name = 'SYNO.MailClient.Thread'
        mailbox = self.get_mailbox_info(mailbox_name='Junk')
        mailbox_id = mailbox.get('id')
        ids, mails = self.get_mails(mailbox_id)
        params = {'method': 'report_spam', 'is_spam': 'false', 'operate_mailbox_id': mailbox_id,
                  'id': f'{ids}', 'conversation_view': 'false'}
        snres_json = self.snapi_requests(api_name, params, method='post')
        return snres_json

    def move_mails(self, fmailbox_id: int, tmailbox_id: int, ids: list):
        api_name = 'SYNO.MailClient.Thread'
        params = {'method': 'set_mailbox', 'id': f"{ids}", 'operate_mailbox_id': f"{fmailbox_id}",  'mailbox_id': f"{tmailbox_id}",
                  'conversation_view': 'false'}

        snres_json = self.snapi_requests(api_name, params, method='post')
        return snres_json

    def drop_dumplicate_mails(self):
        drop_mails = {}
        mailboxes = self.get_mailboxes()

        for mailbox in mailboxes:
            ids = []
            subjects = []
            b_subject, b_bodypreview = None, None
            mailbox_name, mailbox_id = mailbox.get('path'), mailbox.get('id')
            if mailbox_name in ('Trash', 'Junk'):  # 跳过垃圾桶、垃圾邮件
                continue

            # if mailbox_name != 'QQ':
            #     continue

            _ids, mails = self.get_mails(mailbox_id, limit=1000)
            for mail in mails:
                _idx, message = mail.get('id'), mail.get('message')[0]
                _subject, _arrivaltime = message.get('subject'), message.get('arrival_time')
                _subject = f"[{_arrivaltime}]{_subject}"
                _bodypreview = message.get('body_preview')

                if _subject == b_subject and _bodypreview == b_bodypreview:
                    maillogger.warning(f"[{mailbox_name}::{_idx}] duplicate, will be deleted !!! subject: {_subject}")
                    ids.append(_idx)
                    subjects.append(_subject)

                b_subject, b_bodypreview = _subject, _bodypreview

            if ids:
                self.move_mails(fmailbox_id=mailbox_id, tmailbox_id=-6, ids=ids)
                drop_mails[mailbox_name] = list(zip(ids, subjects))
        
        return drop_mails

    def get_mail_info(self, ids: list):
        api_name = 'SYNO.Entry.Request'
        compound = [{"api": "SYNO.MailClient.Message", "method": "get", "id": ids, "additional": ["blockquote", "truncated"]}]
        compound = json.dumps(compound)
        params = {'method': 'request', 'stop_when_error': 'false', 'compound': compound}
        snres_json = self.snapi_requests(api_name, params, method='post')
        return snres_json

    def spam_action(self):
        spam_action = {}
        spam_result = self.spam_report()
        spam_action['spam_result'] = spam_result
        filter_result = self.filter()
        spam_action['filter_result'] = filter_result
        drop_mails = self.drop_dumplicate_mails()
        spam_action['drop_mails'] = drop_mails
        return spam_action
