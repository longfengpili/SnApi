# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-07-20 17:40:35
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-07-20 18:30:29


import os
import json

from snapi.snrequests import SnRequests


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
        with open(self.apifile, 'r', encoding='utf-8') as f:
            apis = json.load(f)

        if api_name not in apis:
            apis = self.get_apis()
        
        api_info = apis.get(api_name)
        return api_info
