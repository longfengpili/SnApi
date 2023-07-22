# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-07-20 17:40:35
# @Last Modified by:   chunyang.xu
# @Last Modified time: 2023-07-22 10:52:45


import os

from snapi.snrequests import SnRequests
from snapi.conf import UpdateApi

import logging
apilogger = logging.getLogger(__name__)


class SnApiModel:

    def __init__(self, name: str, version: str, path: str, **kwargs):
        self.name = name
        self.version = version
        self.path = path

    @staticmethod
    def snapi_fdict(cls, api_name: str, api_info: dict):
        otp = {k: v for k, v in api_info.items() if k not in ('maxVersion', 'path')}
        version = api_info.get('maxVersion')
        urlpath = api_info.get('path')
        return cls(api_name, version, urlpath, kwargs=otp)

    def __repr__(self):
        return f"{self.name}[{self.version}]"


class SnApi(SnRequests):

    def __init__(self, ip_address: str, port: str):
        self.ip_address = ip_address
        self.port = port
        super(SnApi, self).__init__()
        self.apifile = os.path.join(os.getcwd(), 'snapi/conf/apis.json')
        self.updateapi = UpdateApi()

    def get_apis(self):
        api_name = 'SYNO.API.Info'
        urlpath = 'entry.cgi'
        params = {'version': '1', 'method': 'query', 'query': 'all'}
        snres_json = self.sn_requests(urlpath, api_name, params)
        apis = snres_json['data']
        self.updateapi.dump(self.apifile, apis)
        return apis

    def get_api_info(self, api_name: str):
        apis = self.updateapi.load(self.apifile)
        if not apis or api_name not in apis:
            os.remove(self.apifile)
            apis = self.get_apis()
        
        api_info = apis.get(api_name)
        return api_info
