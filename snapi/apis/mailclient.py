# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-07-17 18:46:50
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-09-08 11:02:26


import os
import re
import json
from lxml import etree

from .base import SnBaseApi
from snapi.conf import APISerialize

import logging
maillogger = logging.getLogger(__name__)


class MailModel:

    def __init__(self, source: str, id: int, arrivaltime: int, subject: str, bodypreview: str, **kwargs):
        self.source = source
        self.id = id
        self.arrivaltime = arrivaltime
        self.subject = subject
        self.bodypreview = bodypreview
        self.kwargs = kwargs

    def __repr__(self):
        return f'[{self.arrivaltime}]{self.source}::{self.id}::{self.subject}'

    def __eq__(self, other):
        if isinstance(other, MailModel):
            return (self.arrivaltime == other.arrivaltime and self.subject == other.subject and self.bodypreview == other.bodypreview)

    @property
    def dict(self):
        mail = {'source': self.source, 'id': self.id, 'arrivaltime': self.arrivaltime,
                'subject': self.subject, 'bodypreview': self.bodypreview}

        mail.update(self.kwargs)
        return mail

    @property
    def new_subject(self):
        return f'[{self.arrivaltime}]{self.source}::{self.id}::{self.subject}'

    @staticmethod
    def flatten_dict(d: dict, parent_key: str = None, sep: str = '::'):
        items = []
        if isinstance(d, str):
            items.append((parent_key, d))
            return dict(items)

        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                next_dict = MailModel.flatten_dict(v, new_key, sep=sep)
                items.extend(next_dict.items())
            elif isinstance(v, list):
                for idx, v_elem in enumerate(v):
                    new_key = f'{new_key}{sep}{idx}'
                    next_dict = MailModel.flatten_dict(v_elem, new_key, sep=sep)
                    items.extend(next_dict.items())
            else:
                items.append((new_key, v))
        return dict(items)

    @classmethod
    def parse_mail(cls, mail: dict, source: str = 'mail'):
        def get_value(d: dict, keys: list):
            for key in keys:
                value = d.get(key)
                if value:
                    if key == 'body::html':
                        html = etree.HTML(value)
                        values = html.xpath('//text()')
                        values = [re.sub(r'\s+', '', value) for value in values if value.strip()]
                        value = '\n'.join(values)
                    return value

        mail_flatten = cls.flatten_dict(mail)
        key_mapping = {
            'id': ['message::0::id', 'id'],
            'arrivaltime': ['message::0::arrival_time', 'arrival_time'],
            'subject': ['message::0::subject', 'subject'],
            'bodypreview': ['message::0::body_preview', 'body::html'],
        }
        id = get_value(mail_flatten, key_mapping.get('id'))
        arrivaltime = get_value(mail_flatten, key_mapping.get('arrivaltime'))
        subject = get_value(mail_flatten, key_mapping.get('subject'))
        bodypreview = get_value(mail_flatten, key_mapping.get('bodypreview'))

        mail_flatten = {k: v for k, v in mail_flatten.items() if k not in key_mapping.keys()}
        return cls(source, id, arrivaltime, subject, bodypreview, **mail_flatten)


class MailClient(SnBaseApi):

    def __init__(self, ip_address: str, port: str, username: str, password: str, otp_code: str = None):
        self.app = 'MailClient'
        super(MailClient, self).__init__(self.app, ip_address, port, username, password, otp_code)
        self.api = APISerialize()
        self.mailboxfile = os.path.join(os.getcwd(), 'snapi/conf/mailbox/mailbox.json')

    def get_mailboxes_api(self):
        api_name = 'SYNO.MailClient.Mailbox'
        params = {'method': 'list', 'conversation_view': 'false', 'subscription': 'false', 
                  'additional': ["unread_count", "draft_total_count"]}
        snres_json = self.snapi_requests(api_name, params, method='post')
        mailboxes = snres_json.get('data').get('mailbox')
        self.api.dump(self.mailboxfile, mailboxes)
        return mailboxes

    def get_mailboxes(self):
        mailboxes = self.api.load(self.mailboxfile)
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
        filterfile = os.path.join(os.getcwd(), 'snapi/conf/mailbox/mailfilters.json')
        api_name = 'SYNO.MailClient.Filter'
        params = {'method': 'list'}
        snres_json = self.snapi_requests(api_name, params, method='post')
        filters = snres_json.get('data').get('filter')
        self.api.dump(filterfile, filters)
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

    def get_mails(self, mailbox_id: int = -1, offset: int = 0, limit: int = 200, getmax: int = 400):
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
        while _mails and offset < getmax:
            mails.extend(_mails)
            ids.extend(_ids)
            offset += limit
            params['offset'] = offset
            snres_json = self.snapi_requests(api_name, params, method='post')
            _mails = snres_json.get('data').get('thread')
            _ids = snres_json.get('data').get('matched_ids')

        mails = [MailModel.parse_mail(mail) for mail in mails]
        counts = len(mails)
        mailbox = self.get_mailbox_info(mailbox_id=mailbox_id)
        mailbox_name = mailbox.get('path')
        maillogger.info(f"[{mailbox_name}]has email {counts} counts ! ")
        return ids, mails

    def spam_report(self):
        snres_json = None
        api_name = 'SYNO.MailClient.Thread'
        mailbox = self.get_mailbox_info(mailbox_name='Junk')
        mailbox_id = mailbox.get('id')
        ids, mails = self.get_mails(mailbox_id)

        if ids:
            subjects = [mail.new_subject for mail in mails]
            params = {'method': 'report_spam', 'is_spam': 'false', 'operate_mailbox_id': mailbox_id,
                      'id': f'{ids}', 'conversation_view': 'false'}
            snres_json = self.snapi_requests(api_name, params, method='post')
            snres_json['info'] = tuple(zip(ids, subjects))
        return snres_json

    def move_mails(self, fmailbox_id: int, tmailbox_id: int, ids: list):
        api_name = 'SYNO.MailClient.Thread'
        params = {'method': 'set_mailbox', 'id': f"{ids}", 'operate_mailbox_id': f"{fmailbox_id}",  'mailbox_id': f"{tmailbox_id}",
                  'conversation_view': 'false'}

        snres_json = self.snapi_requests(api_name, params, method='post')
        return snres_json

    def drop_dumplicate_mails(self, check_mailbox_name: str = None, check_max: int = 1000):
        def parse_mail(mail: dict):
            idx, message = mail.get('id'), mail.get('message')[0]
            subject, arrivaltime, bodypreview = message.get('subject'), message.get('arrival_time'), message.get('body_preview')
            subject = f"[{arrivaltime}]{subject}"
            return idx, subject, bodypreview

        drop_mails = {}
        mailboxes = self.get_mailboxes()

        for mailbox in mailboxes:
            ids, subjects = [], []
            mailbox_name, mailbox_id = mailbox.get('path'), mailbox.get('id')
            # maillogger.info(f"{mailbox}")

            if mailbox_name in ('Trash', 'Junk'):  # 跳过垃圾桶、垃圾邮件
                continue
            if check_mailbox_name and mailbox_name != check_mailbox_name:
                continue

            _ids, mails = self.get_mails(mailbox_id, limit=1000, getmax=check_max)
            mails_combine = zip(mails[:-1], mails[1:])
            for mails in mails_combine:
                f_mail, s_mail = mails
                if f_mail == s_mail:
                    id, new_subject = s_mail.id, s_mail.new_subject
                    maillogger.warning(f"[{mailbox_name}::{mailbox_id}::{id}] duplicate, will be deleted !!! subject: {new_subject}")
                    ids.append(id)
                    subjects.append(new_subject)

            if ids:
                self.move_mails(fmailbox_id=mailbox_id, tmailbox_id=-6, ids=ids)
                drop_mails[mailbox_name] = list(zip(ids, subjects))
        
        return drop_mails

    def get_messages(self, ids: list):
        api_name = 'SYNO.Entry.Request'
        compound = [{"api": "SYNO.MailClient.Message", "method": "get", "id": ids, "additional": ["blockquote", "truncated"]}]
        compound = json.dumps(compound)
        params = {'method': 'request', 'stop_when_error': 'false', 'compound': compound}
        snres_json = self.snapi_requests(api_name, params, method='post')
        messages = snres_json.get('data').get('result')[0].get('data').get('message')
        messages = [MailModel.parse_mail(message, source='message').dict for message in messages]
        return messages

    def spam_action(self, check_max: int = 1000):
        spam_action = {}
        spam_result = self.spam_report()
        spam_action['spam_result'] = spam_result
        filter_result = self.filter()
        spam_action['filter_result'] = filter_result
        drop_mails = self.drop_dumplicate_mails(check_max=check_max)
        spam_action['drop_mails'] = drop_mails

        return spam_action
