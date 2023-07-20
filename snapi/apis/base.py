# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-07-17 16:47:30
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-07-20 18:51:53

import json

from .apis import SnApi
from snapi.snrequests import SnRequests
from snapi.auth import SynologyAuth


class SnBaseApi(SnRequests):

    def __init__(self, app: str, ip_address: str, port: str, username: str, password: str, otp_code: str = None):
        self.app = app
        self.ip_address = ip_address
        self.port = port
        self.username = username
        self.password = password
        self.otp_code = otp_code
        super(SnBaseApi, self).__init__()

    @property
    def errors(self):
        return 

    @property
    def sid(self):
        snauth = SynologyAuth(self.ip_address, self.port, self.username, self.password)
        sid = snauth.login(self.app)
        return sid

    def get_api_info(self, api_name: str):
        apis = SnApi(self.ip_address, self.port)
        api_info = apis.get_api_info(api_name)
        return api_info

    def snapi_requests(self, api_name: str, params: str, method: str = 'get'):
        sid = self.sid
        api_info = self.get_api_info(api_name)
        urlpath, version = api_info.get('path'), api_info.get('maxVersion')
        params['version'] = version
        snres_json = self.sn_requests(urlpath, api_name, params, sid=sid, method=method)
        return snres_json
