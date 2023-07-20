# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-07-20 17:40:35
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-07-20 18:51:33


import os
import json

from snapi.snrequests import SnRequests

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
        self.apifile = os.path.join(os.getcwd(), 'snapi/conf/apis.json')
        self.ip_address = ip_address
        self.port = port
        super(SnApi, self).__init__()

    def get_apis(self):
        api_name = 'SYNO.API.Info'
        urlpath = 'entry.cgi'
        params = {'version': '1', 'method': 'query', 'query': 'all'}
        snres_json = self.sn_requests(urlpath, api_name, params)
        apis = snres_json['data']

        with open(self.apifile, 'w', encoding='utf-8') as f:
            json.dump(apis, f, indent=2, ensure_ascii=False)
        return apis

    def get_api_info(self, api_name: str):
        apis = None
        with open(self.apifile, 'r', encoding='utf-8') as f:
            try:
                apis = json.load(f)
            except json.decoder.JSONDecodeError as e:
                apilogger.error(f"Load file[{self.apifile}] error, message: {e}")

        if not apis or api_name not in apis:
            os.remove(self.apifile)
            apis = self.get_apis()
        
        api_info = apis.get(api_name)
        return api_info
