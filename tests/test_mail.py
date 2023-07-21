# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-07-17 14:27:27
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-07-21 15:56:49

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

    def data_dump(self, data: dict):
        with open('./tests/mail.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def test_filter(self):
        snres_json = self.mailclient.filter()
        print(snres_json)

    def test_spam_list(self):
        snres_json = self.mailclient.get_spams()
        self.data_dump(snres_json)

    def test_spam_report(self):
        snres_json = self.mailclient.spam_report()
        print(snres_json)

    def test_mailboxes(self):
        snres_json = self.mailclient.get_mailboxes()
        self.data_dump(snres_json)

    def test_maillabels(self):
        snres_json = self.mailclient.get_maillabels()
        self.data_dump(snres_json)

    def test_get_filters(self):
        snres_json = self.mailclient.get_filters()
        self.data_dump(snres_json)

    def test_get_mails(self):
        id = [49473, 49470]
        snres_json = self.mailclient.get_mails(id)
        self.data_dump(snres_json)
