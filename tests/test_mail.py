# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-07-17 14:27:27
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-07-20 17:32:26

import json
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

    def test_spam_list(self):
        snres_json = self.mailclient.get_spam_list()
        with open('./tests/dustbin_list.json', 'w', encoding='utf-8') as f:
            json.dump(snres_json, f, indent=2, ensure_ascii=False)

    def test_spam_report(self):
        snres_json = self.mailclient.spam_report()
        print(snres_json)
