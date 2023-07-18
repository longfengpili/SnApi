# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-07-17 14:27:27
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-07-18 11:32:33


from snapi.auth import SynologyAuth

from .test_conf import IP_ADDRESS, PORT, USERNAME, PASSWORD


class TestAuth:

    def setup_method(self, method):
        ip_address = IP_ADDRESS
        port = PORT
        username = USERNAME
        password = PASSWORD
        self.snauth = SynologyAuth(ip_address, port, username, password)

    def teardown_method(self, method):
        pass

    def test_login(self):
        sid = self.snauth.login(app='test')
        print(sid)

    def test_logout(self):
        _ = self.snauth.logout(app='test')

    def test_get_apis(self):
        app = 'SYNO.MailClient'
        apis = self.snauth.get_apis(app=app)
        print(apis)
