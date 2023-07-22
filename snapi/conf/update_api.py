# -*- coding: utf-8 -*-
# @Author: chunyang.xu
# @Date:   2023-07-22 09:54:04
# @Last Modified by:   chunyang.xu
# @Last Modified time: 2023-07-22 10:33:29


import os
import json

import logging
conflogger = logging.getLogger(__name__)


class UpdateApi:

    def __init__(self, apifile: str):
        self.apifile = apifile

    def dump(self, apis: dict):
        with open(self.apifile, 'w', encoding='utf-8') as f:
            json.dump(apis, f, indent=2, ensure_ascii=False)

    def load(self):
        apis = None
        if os.path.exists(self.apifile):
            with open(self.apifile, 'r', encoding='utf-8') as f:
                try:
                    apis = json.load(f)
                except json.decoder.JSONDecodeError as e:
                    conflogger.error(f"Load file[{self.apifile}] error, message: {e}")
        else:
            self.dump(apis={})
        return apis
