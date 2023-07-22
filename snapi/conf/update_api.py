# -*- coding: utf-8 -*-
# @Author: chunyang.xu
# @Date:   2023-07-22 09:54:04
# @Last Modified by:   chunyang.xu
# @Last Modified time: 2023-07-22 16:34:02


import os
import json

import logging
conflogger = logging.getLogger(__name__)


class UpdateApi:

    def __init__(self):
        pass

    def dump(self, apifile: str, apis: dict):
        # if os.path.exists(apifile):
        #     os.remove(apifile)

        with open(apifile, 'w', encoding='utf-8') as f:
            json.dump(apis, f, indent=2, ensure_ascii=False)

    def load(self, apifile):
        if not os.path.exists(apifile):
            return

        with open(apifile, 'r', encoding='utf-8') as f:
            try:
                apis = json.load(f)
            except json.decoder.JSONDecodeError as e:
                conflogger.error(f"Load file[{apifile}] error, message: {e}")
                apis = None
        return apis
