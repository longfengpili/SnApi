# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-07-17 18:46:50
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-11-24 10:18:03


import os
import re
import json
from lxml import etree

from .base import SnBaseApi
from snapi.conf import APISerialize

import logging
callogger = logging.getLogger(__name__)


class CalClient(SnBaseApi):

    def __init__(self, ip_address: str, port: str, username: str, password: str, otp_code: str = None):
        self.app = 'CalClient'
        super(CalClient, self).__init__(self.app, ip_address, port, username, password, otp_code)
        self.api = APISerialize()

    def get_cal(self):
        api_name = 'SYNO.Cal.Event'
        params = {'method': 'list', 'version': '1', 'start': 1698768000, 
                  'end': 1701360000, 'list_repeat': 'true',
                  'cal_id_list': ["/longfengpili/home/", "/longfengpili/ygpeixi/"]}
        snres_json = self.snapi_requests(api_name, params, method='post')
        return snres_json
