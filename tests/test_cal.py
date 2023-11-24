# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-11-24 09:53:57
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-11-24 09:56:19
# @github: https://github.com/longfengpili


import json
import pytest

from snapi.apis import CalClient
from .test_conf import IP_ADDRESS, PORT, USERNAME, PASSWORD


class TestCalClient:

    def setup_method(self, method):
        ip_address = IP_ADDRESS
        port = PORT
        username = USERNAME
        password = PASSWORD
        self.calclient = CalClient(ip_address, port, username, password)

    def teardown_method(self, method):
        pass

    def test_get_cal(self):
        res = self.calclient.get_cal()
        print(res)