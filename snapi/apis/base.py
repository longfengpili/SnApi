# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-07-17 16:47:30
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-07-18 18:57:20


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
        self.snauth = SynologyAuth(self.ip_address, self.port, self.username, self.password, otp_code=self.otp_code)

    @property
    def sid(self):
        sid = self.snauth.login(self.app)
        return sid

    @property
    def apis(self):
        api_name = 'SYNO.API.Info'
        urlpath = 'entry.cgi'
        params = {'version': '1', 'method': 'query', 'query': 'all'}
        snres_json = self.sn_requests(urlpath, api_name, params)
        apis = snres_json['data']
        return apis

    def get_api_info(self, api_name: str):
        api_info = self.apis.get(api_name)
        return api_info

    def get_api_version(self, api_name: str):
        api_info = self.apis.get(api_name)
        version = api_info.get('maxVersion')
        return version

    def get_api_urlpath(self, api_name: str):
        api_info = self.apis.get(api_name)
        urlpath = api_info.get('path')
        return urlpath
