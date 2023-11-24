# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-07-17 17:12:49
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-11-24 10:11:16


import requests
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

from snapi.exceptions import BASE_ERRORS
from snapi.exceptions import SynoError

import logging
snrequestlogger = logging.getLogger(__name__)


class SnRequests:
    '''https://www.synology.cn/zh-cn/support/developer#tool'''

    def __init__(self, cert_verify: bool = False, dsm_version: int = 7):
        self.verify = cert_verify
        self.version = dsm_version

        if self.verify is False:
            disable_warnings(InsecureRequestWarning)

    @property
    def baseurl(self):
        baseurl = f'https://{self.ip_address}:{self.port}/webapi'
        return baseurl

    @property
    def errors(self):
        return 

    def sn_requests(self, urlpath: str, api_name: str, params: dict, sid: str = None, method: str = 'get'):
        def request_by_method(method: str, url: str, params: dict, data: dict = None):
            if method == 'post':
                snres = requests.post(url, data=params, verify=self.verify)
            else:
                snres = requests.get(url, params=params, verify=self.verify)

            snrequestlogger.debug(f"[{method.upper()}]{snres.url}, params: {params}")
            return snres

        params['api'] = api_name
        params['_sid'] = sid
        url = f"{self.baseurl}/{urlpath}"
        # snrequestlogger.debug(f"[{method.upper()}::{api_name}]{url}")
        snres = request_by_method(method, url, params)
        snres_json = snres.json()
        # snrequestlogger.info(snres_json)

        snres_info = f"[{method}]{snres.url}" if method == 'get' else f"[{method}]{snres.url}, params: {params}"
        self.judge_error(snres_json, snres_info)

        return snres_json

    def judge_error(self, response: dict[str, object], request_info: str):
        # code, message = 200, 'success'
        error = response.get('error')
        if error:
            code = error.get('code')
            message = error.get('errors')
            if not message:
                errors = BASE_ERRORS | self.errors if self.errors else BASE_ERRORS
                message = errors.get(code)
            message = f"{message}, [request_info]{request_info}"
            raise SynoError(code, message)
