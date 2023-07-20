# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-07-17 14:27:27
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-07-20 16:27:51


import pytest

from snapi.apis import MailClient

from .test_conf import IP_ADDRESS, PORT, USERNAME, PASSWORD


class TestMailClient:

    def setup_method(self, method):
        ip_address = IP_ADDRESS
        port = PORT
        username = USERNAME
        password = PASSWORD
        self.mailclient = MailClient(ip_address, port, username, password)

    def teardown_method(self, method):
        pass

    def test_filter(self):
        condition = '[{"name":"subject","value":"QQ OR 腾讯"}]'
        action = '[{"name":"move_to","value":"7"},{"name":"set_label","value":"6"}]'
        snres_json = self.mailclient.filter(condition, action)
        print(snres_json)
