# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-11-24 10:26:15
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-11-24 10:28:18
# @github: https://github.com/longfengpili


import json
import pytest

from snapi.apis import SnApi
from .test_conf import IP_ADDRESS, PORT, USERNAME, PASSWORD


class TestSnApi:

    def setup_method(self, method):
        ip_address = IP_ADDRESS
        port = PORT
        self.apis = SnApi(ip_address, port)

    def teardown_method(self, method):
        pass

    def test_get_apis(self):
        res = self.apis.get_apis()
        print(res)
