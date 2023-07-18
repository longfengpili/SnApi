# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-07-14 15:52:43
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-07-18 18:58:18


import threading

from snapi.snrequests import SnRequests


class SynologyAuth(SnRequests):
    _instance_lock = threading.Lock()

    def __init__(self, ip_address: str, port: str, username: str, password: str, otp_code: str = None):
        self.ip_address: str = ip_address
        self.port: str = port
        self.username: str = username
        self.password: str = password
        self.otp_code = otp_code
        super(SynologyAuth, self).__init__()

    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(SynologyAuth, '_instance'):
    #         with SynologyAuth._instance_lock:
    #             if not hasattr(SynologyAuth, '_instance'):
    #                 SynologyAuth._instance = super().__new__(cls)
    #     return SynologyAuth._instance

    @property
    def api_name(self):
        api_name = 'SYNO.API.Auth'
        return api_name

    @property
    def urlpath(self):
        urlpath = 'entry.cgi'
        return urlpath

    def login(self, app: str):
        urlpath, api_name = self.urlpath, self.api_name

        params = {'version': self.version, 'method': 'login', 'account': self.username,
                  'passwd': self.password, 'format': 'cookie', 'session': app}
        if self.otp_code:
            params['otp_code'] = self.otp_code
        if not self.sid:
            snres_json = self.sn_requests(urlpath, api_name, params)
            sid = snres_json['data']['sid']
            self.sid = sid
        return self.sid

    def logout(self, app: str):
        params = {'version': self.version, 'method': 'logout', 'session': app}
        urlpath, api_name = self.urlpath, self.api_name
        _ = self.sn_requests(urlpath, api_name, params)
        # self.sid = None
        return
