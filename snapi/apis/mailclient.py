# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-07-17 18:46:50
# @Last Modified by:   chunyang.xu
# @Last Modified time: 2023-07-22 10:34:16


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
        self.mailboxfile = os.path.join(os.getcwd(), 'snapi/conf/mailbox/mailbox.json')
        self.update_mailbox_api = UpdateApi(self.mailboxfile)

    def get_mailboxes(self):
        api_name = 'SYNO.MailClient.Mailbox'
        params = {'method': 'list', 'conversation_view': 'false', 'subscription': 'false', 
                  'additional': ["unread_count", "draft_total_count"]}
        snres_json = self.snapi_requests(api_name, params, method='post')
        mailboxes = snres_json.get('data').get('mailbox')
        self.update_mailbox_api.dump(mailboxes)
        return mailboxes

    def get_mailbox_info(self, mailbox: str):
        mailboxes = self.update_mailbox_api.load()
        if not mailboxes:
            os.remove(self.mailboxfile)
            mailboxes = self.get_mailboxes()
    
        mailboxes = [mbox for mbox in mailboxes if mbox.get('path') == mailbox]
        return mailboxes

    def get_maillabels(self):
        api_name = 'SYNO.MailClient.Label'
        params = {'method': 'list', 'conversation_view': 'false'}
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

    def get_mails(self, mailbox: str = 'INBOX'):
        api_name = 'SYNO.MailClient.Thread'
        mailboxes = self.get_mailbox_info(mailbox)
        mailbox_id = mailboxes[0].get('id')
        condition = [{"name": "mailbox", "value": f"{mailbox_id}"}]
        condition = self.convert_to_json(condition)
        params = {'method': 'list', 'offset': '0', 'limit': '200', 'condition': condition, 'conversation_view': 'false'}
        snres_json = self.snapi_requests(api_name, params, method='post')
        return snres_json

    # def move_mails(self, fmailbox: str, tmailbox: str, id: list):




    # api: SYNO.MailClient.Thread
    # method: set_mailbox
    # version: 10
    # id: [47677,47666]
    # mailbox_id: -6
    # operate_mailbox_id: -1
    # conversation_view: false



    def spam_report(self):
        api_name = 'SYNO.MailClient.Thread'
        res_json = self.get_mails(mailbox='Junk')
        spams = res_json.get('data').get('matched_ids')
        params = {'method': 'report_spam', 'is_spam': 'false', 
                  'id': f'{spams}', 'conversation_view': 'false'}
        snres_json = self.snapi_requests(api_name, params, method='post')
        return snres_json

    def get_mail_info(self, id: list):
        api_name = 'SYNO.Entry.Request'
        compound = [{"api": "SYNO.MailClient.Message", "method": "get", "id": id, "additional": ["blockquote", "truncated"]}]
        compound = json.dumps(compound)
        params = {'method': 'request', 'stop_when_error': 'false', 'compound': compound}
        snres_json = self.snapi_requests(api_name, params, method='post')
        return snres_json
