# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-07-18 12:16:02
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-07-18 13:27:27


from snapi.apis import SnBaseApi

from .test_conf import IP_ADDRESS, PORT, USERNAME, PASSWORD


class TestSnBaseApi:

    def setup_method(self, method):
        ip_address = IP_ADDRESS
        port = PORT
        username = USERNAME
        password = PASSWORD
        self.snapi = SnBaseApi('test', ip_address, port, username, password)

    def teardown_method(self, method):
        pass

    def test_login(self):
        sid = self.snapi.sid
        print(sid)
