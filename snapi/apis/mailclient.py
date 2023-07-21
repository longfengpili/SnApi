# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-07-17 18:46:50
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-07-21 17:29:48


import json

from .base import SnBaseApi


class MailClient(SnBaseApi):

    def __init__(self, ip_address: str, port: str, username: str, password: str, otp_code: str = None):
        self.app = 'MailClient'
        super(MailClient, self).__init__(self.app, ip_address, port, username, password, otp_code)

    def get_mailboxes(self):
        api_name = 'SYNO.MailClient.Mailbox'
        params = {'method': 'list', 'conversation_view': 'false', 'subscription': 'false', 
                  'additional': ["unread_count", "draft_total_count"]}
        snres_json = self.snapi_requests(api_name, params, method='post')
        return snres_json

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

    def get_spams(self):
        api_name = 'SYNO.MailClient.Thread'
        condition = [{"name": "mailbox", "value": "-5"}]
        condition = self.convert_to_json(condition)
        params = {'method': 'list', 'offset': '0', 'limit': '200', 'condition': condition, 'conversation_view': 'false'}
        snres_json = self.snapi_requests(api_name, params, method='post')
        spam_list = snres_json.get('data').get('matched_ids')
        return spam_list

    def spam_report(self):
        api_name = 'SYNO.MailClient.Thread'
        spam_list = self.get_spams()
        params = {'method': 'report_spam', 'is_spam': 'false', 
                  'id': f'{spam_list}', 'conversation_view': 'false'}
        snres_json = self.snapi_requests(api_name, params, method='post')
        return snres_json

    def get_mails(self, id: list):
        api_name = 'SYNO.Entry.Request'
        compound = [{"api": "SYNO.MailClient.Message", "method": "get", "id": id, "additional": ["blockquote", "truncated"]}]
        compound = json.dumps(compound)
        params = {'method': 'request', 'stop_when_error': 'false', 'compound': compound}
        snres_json = self.snapi_requests(api_name, params, method='post')
        return snres_json
