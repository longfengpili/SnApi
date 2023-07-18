# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-07-17 17:12:49
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-07-18 18:53:01


import requests
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

from snapi.exceptions import CODE_SUCCESS, ERROR_CODES, AUTH_ERROR_CODES
# from snapi.exceptions import DOWNLOAD_STATION_ERROR_CODES, VIRTUALIZATION_ERROR_CODES, FILE_STATION_ERROR_CODES
from snapi.exceptions import SynoConnectionError, HTTPError, JSONDecodeError, LoginError

import logging
snrequestlogger = logging.getLogger('request')


class SnRequests:

    def __init__(self, cert_verify: bool = False, dsm_version: int = 7):
        self.verify = cert_verify
        self.version = dsm_version
        self._sid = None

        if self.verify is False:
            disable_warnings(InsecureRequestWarning)

    @property
    def baseurl(self):
        baseurl = f'https://{self.ip_address}:{self.port}/webapi'
        return baseurl

    @property
    def sid(self):
        return self._sid

    @sid.setter
    def sid(self, sid):
        self._sid = sid

    def sn_requests(self, urlpath: str, api_name: str, params: dict, method: str = 'get'):
        def request_by_method(method: str, url: str, params: dict, data: dict = None):
            if method == 'post':
                snres = requests.post(url, params, verify=self.verify)
            else:
                snres = requests.get(url, params, verify=self.verify)

            snrequestlogger.debug(f"[{method.upper()}]{snres.url}, params: {params}")
            return snres

        params['api'] = api_name
        params['_sid'] = self.sid
        url = f"{self.baseurl}/{urlpath}"
        # snrequestlogger.debug(f"[{method.upper()}::{api_name}]{url}")
        try:
            snres = request_by_method(method, url, params)
            snres.raise_for_status()
            snres_json = snres.json()
            # snrequestlogger.info(snres_json)
        except requests.exceptions.ConnectionError as e:
            raise SynoConnectionError(error_message=e.args[0])
        except requests.exceptions.HTTPError as e:
            raise HTTPError(error_message=str(e.args))
        except requests.exceptions.JSONDecodeError as e:
            raise JSONDecodeError(error_message=str(e.args))

        error_code = self.get_error_code(snres_json)
        if error_code:
            raise LoginError(error_code)
        return snres_json

    @staticmethod
    def get_error_code(response: dict[str, object]):
        if response.get('success'):
            code = CODE_SUCCESS
        else:
            code = response.get('error').get('code')
        return code
