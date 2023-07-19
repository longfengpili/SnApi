# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-07-17 16:47:30
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-07-19 11:43:22


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
    def sid(self):
        snauth = SynologyAuth(self.ip_address, self.port, self.username, self.password, otp_code=self.otp_code)
        sid = snauth.login(self.app)
        return sid

    @property
    def apis(self):
        api_name = 'SYNO.API.Info'
        urlpath = 'entry.cgi'
        params = {'version': '1', 'method': 'query', 'query': 'all'}
        snres_json = self.sn_requests(urlpath, api_name, params)
        apis = snres_json['data']
        return apis

    def sn_requests_with_sid(self, urlpath: str, api_name: str, params: str, method: str = 'get'):
        snres_json = self.sn_requests(urlpath, api_name, params, sid=self.sid, method=method)
        return snres_json

    def get_api_info(self, api_name: str):
        api_info = self.apis.get(api_name)
        return api_info
