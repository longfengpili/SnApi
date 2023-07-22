# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-07-17 16:47:30
# @Last Modified by:   chunyang.xu
# @Last Modified time: 2023-07-22 14:46:29

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

    def convert_to_json(self, data: any):
        def to_str(value):
            if isinstance(value, bool):
                return value
            if isinstance(value, int):
                return str(value)
            
            return value

        if isinstance(data, list):
            datas = []
            for d in data:
                d = {k: to_str(v) for k, v in d.items()}
                datas.append(d)
        elif isinstance(data, dict):
            datas = {k: to_str(v) for k, v in data.items()}
        else:
            datas = data
        datas = json.dumps(datas, ensure_ascii=False)
        return datas
