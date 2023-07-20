# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-07-17 16:47:30
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-07-20 16:32:10


from snapi.snrequests import SnRequests
from snapi.auth import SynologyAuth


class SnBaseApi(SnRequests):

    def __init__(self, api_base: str, ip_address: str, port: str, username: str, password: str, otp_code: str = None):
        self.api_base = api_base
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
    def app(self):
        app = self.api_base.split('.')[-2]
        return app

    @property
    def sid(self):
        snauth = SynologyAuth(self.ip_address, self.port, self.username, self.password, otp_code=self.otp_code)
        sid = snauth.login(self.app)
        return sid

    @property
    def apis(self):
        query = self.api_base or 'all'
        api_name = 'SYNO.API.Info'
        urlpath = 'entry.cgi'
        params = {'version': '1', 'method': 'query', 'query': query}
        snres_json = self.sn_requests(urlpath, api_name, params)
        apis = snres_json['data']
        return apis

    def snapi_requests(self, urlpath: str, api_name: str, params: str, method: str = 'get'):
        sid = self.sid
        snres_json = self.sn_requests(urlpath, api_name, params, sid=sid, method=method)
        return snres_json

    def get_api_info(self, api_name: str):
        api_info = self.apis.get(api_name)
        return api_info
