# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-07-17 18:46:50
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-07-20 17:36:37

from .base import SnBaseApi


class MailClient(SnBaseApi):

    def __init__(self, ip_address: str, port: str, username: str, password: str, otp_code: str = None):
        self.app = 'MailClient'
        super(MailClient, self).__init__(self.app, ip_address, port, username, password, otp_code)

    def filter(self, condition: str, action: str):
        api_name = 'SYNO.MailClient.Filter'
        params = {'method': 'set', 'session': self.app,
                  'condition': condition, 'action': action, 'id': '13'}
        snres_json = self.snapi_requests(api_name, params, method='post')
        return snres_json

    def get_spam_list(self):
        api_name = 'SYNO.MailClient.Thread'
        condition = '[{"name":"mailbox","value":"-5"}]'
        params = {'method': 'list', 'offset': '0', 'limit': '200', 'condition': condition, 'conversation_view': 'false'}
        snres_json = self.snapi_requests(api_name, params, method='post')
        spam_list = snres_json.get('data').get('matched_ids')
        return spam_list

    def spam_report(self):
        api_name = 'SYNO.MailClient.Thread'
        spam_list = self.get_spam_list()
        params = {'method': 'report_spam', 'is_spam': 'false', 
                  'id': f'{spam_list}', 'conversation_view': 'false'}
        snres_json = self.snapi_requests(api_name, params, method='post')
        return snres_json
