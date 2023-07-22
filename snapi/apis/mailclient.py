# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-07-17 18:46:50
# @Last Modified by:   chunyang.xu
# @Last Modified time: 2023-07-22 13:08:52


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

    def get_mailboxes(self):
        api_name = 'SYNO.MailClient.Mailbox'
        params = {'method': 'list', 'conversation_view': 'false', 'subscription': 'false', 
                  'additional': ["unread_count", "draft_total_count"]}
        snres_json = self.snapi_requests(api_name, params, method='post')
        mailboxes = snres_json.get('data').get('mailbox')
        self.update_mailbox_api.dump(self.mailboxfile, mailboxes)
        return mailboxes

    def get_mailboxex_info(self, mailbox: str = None):
        mailboxes = self.update_mailbox_api.load(self.mailboxfile)
        if not mailboxes:
            os.remove(self.mailboxfile)
            mailboxes = self.get_mailboxes()
        
        if mailbox:
            mailboxes = [mbox for mbox in mailboxes if mbox.get('path') == mailbox]
        return mailboxes

    def get_maillabels(self):
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

    def filter(self):
        results = {}
        api_name = 'SYNO.MailClient.Filter'
        filters = self.get_filters()
        for f in filters:
            enabled, condition, action, idx = f.get('enabled'), f.get('condition'), f.get('action'), f.get('id')
            condition = self.convert_to_json(condition)
            action = self.convert_to_json(action)
            if enabled:
                params = {'method': 'set', 'condition': condition, 'action': action, 'id': idx}
                snres_json = self.snapi_requests(api_name, params, method='post')
                results[idx] = {'result': snres_json, 'condition': condition, 'action': action}
        return results

    def get_mails(self, mailbox_id: int = -1, limit: int = 200):
        api_name = 'SYNO.MailClient.Thread'
        condition = [{"name": "mailbox", "value": f"{mailbox_id}"}]
        condition = self.convert_to_json(condition)
        params = {'method': 'list', 'offset': '0', 'limit': f'{limit}', 'condition': condition, 'conversation_view': 'false'}
        snres_json = self.snapi_requests(api_name, params, method='post')
        return snres_json

    def spam_report(self):
        api_name = 'SYNO.MailClient.Thread'
        mailboxes = self.get_mailboxex_info(mailbox='Junk')
        mailbox_id = mailboxes[0].get('id')
        res_json = self.get_mails(mailbox_id)
        spams = res_json.get('data').get('matched_ids')
        params = {'method': 'report_spam', 'is_spam': 'false', 
                  'id': f'{spams}', 'conversation_view': 'false'}
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
        mailboxes = self.get_mailboxex_info()

        for mailbox in mailboxes:
            ids = []
            subjects = []
            b_subject, b_bodypreview = None, None
            name, idx = mailbox.get('path'), mailbox.get('id')
            if name in ('Trash', 'Junk'):  # 跳过垃圾桶、垃圾邮件
                continue

            res_json = self.get_mails(idx, limit=20000)
            threads = res_json.get('data').get('thread')
            for thread in threads:
                # print(thread)
                _idx, message = thread.get('id'), thread.get('message')[0]
                _subject, _arrivaltime = message.get('subject'), message.get('arrival_time')
                _subject = f"[{_arrivaltime}]{_subject}"
                _bodypreview = message.get('body_preview')

                if _subject == b_subject and _bodypreview == b_bodypreview:
                    maillogger.warning(f"[{name}::{_idx}] duplicate, will be deleted !!! subject: {_subject}")
                    ids.append(_idx)
                    subjects.append(_subject)

                b_subject, b_bodypreview = _subject, _bodypreview

            if ids:
                self.move_mails(fmailbox_id=idx, tmailbox_id=-6, ids=ids)
                drop_mails[name] = list(zip(ids, subjects))
        
        return drop_mails

    def get_mail_info(self, ids: list):
        api_name = 'SYNO.Entry.Request'
        compound = [{"api": "SYNO.MailClient.Message", "method": "get", "id": ids, "additional": ["blockquote", "truncated"]}]
        compound = json.dumps(compound)
        params = {'method': 'request', 'stop_when_error': 'false', 'compound': compound}
        snres_json = self.snapi_requests(api_name, params, method='post')
        return snres_json
