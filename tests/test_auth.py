# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-07-17 14:27:27
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-07-19 10:52:20


from snapi.auth import SynologyAuth

from .test_conf import IP_ADDRESS, PORT, USERNAME, PASSWORD


class TestAuth:

    def setup_method(self, method):
        self.ip_address = IP_ADDRESS
        self.port = PORT
        self.username = USERNAME
        self.password = PASSWORD

    def teardown_method(self, method):
        pass

    def test_login(self):
        snauth = SynologyAuth(self.ip_address, self.port, self.username, self.password)
        sid = snauth.login(app='test')
        print(sid)

    def test_login2(self):
        snauth1 = SynologyAuth(self.ip_address, self.port, self.username, self.password)
        sid1 = snauth1.login(app='test')
        print(id(snauth1), sid1)
        snauth2 = SynologyAuth(self.ip_address, self.port, self.username, self.password)
        sid2 = snauth2.login(app='test')
        print(id(snauth2), sid2)

    def test_logout(self):
        snauth = SynologyAuth(self.ip_address, self.port, self.username, self.password)
        _ = snauth.logout(app='test')
