# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-07-17 18:46:50
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-07-20 14:36:53


from .base import SnBaseApi


class MailClient(SnBaseApi):

    def __init__(self, ip_address: str, port: str, username: str, password: str, otp_code: str = None):
        self.api_base = 'SYNO.MailClient.'
        super(MailClient, self).__init__(self.api_base, ip_address, port, username, password, otp_code)

    def filter(self, condition: str, action: str):
        api_name = 'SYNO.MailClient.Filter'
        api_info = self.get_api_info(api_name)
        urlpath = api_info.get('path')
        version = api_info.get('maxVersion')
        params = {'version': version, 'method': 'set', 'session': self.app,
                  'condition': condition, 'action': action, 'id': '13'}
        snres_json = self.snapi_requests(urlpath, api_name, params, method='post')
        return snres_json
