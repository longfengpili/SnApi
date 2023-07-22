# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-07-17 14:27:27
# @Last Modified by:   chunyang.xu
# @Last Modified time: 2023-07-22 21:13:04

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

    def test_get_filters(self):
        snres_json = self.mailclient.get_filters()
        self.data_dump(snres_json)

    def test_filter_act(self):
        condition = [{"name": "to", "value": "398745129@qq.com"}]
        action = [{"name": "move_to", "value": "7"}, {"name": "set_label", "value": "6"}]
        idx = 15
        snres_json = self.mailclient.filter_act(condition, action, idx)
        self.data_dump(snres_json)

    def test_filter(self):
        snres_json = self.mailclient.filter()
        self.data_dump(snres_json)

    def test_get_mails(self):
        mails = self.mailclient.get_mails(mailbox_id=-1, offset=0, limit=1000)
        self.data_dump(mails)

    def test_spam_report(self):
        snres_json = self.mailclient.spam_report()
        self.data_dump(snres_json)

    def test_spam_action(self):
        snres_json = self.mailclient.spam_action()
        self.data_dump(snres_json)

    def test_mailboxes(self):
        snres_json = self.mailclient.get_mailboxes()
        self.data_dump(snres_json)

    def test_get_mailbox_info(self):
        snres_json = self.mailclient.get_mailbox_info(mailbox_name='Trash')
        self.data_dump(snres_json)

    def test_maillabels_api(self):
        snres_json = self.mailclient.get_maillabels_api()
        self.data_dump(snres_json)

    def test_get_mail_info(self):
        id = [49473, 49470]
        snres_json = self.mailclient.get_mail_info(id)
        self.data_dump(snres_json)

    def test_drop_dumplicate_mails(self):
        drop_mails = self.mailclient.drop_dumplicate_mails()
        self.data_dump(drop_mails)
