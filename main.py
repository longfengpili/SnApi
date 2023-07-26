# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-07-25 15:09:36
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-07-26 10:49:39

import os
from snapi.apis import MailClient


env = os.environ
ip_address = env.get('IP_ADDRESS')
port = env.get('PORT')
username = env.get('USERNAME')
password = env.get('PASSWORD')

if not ip_address:
    try:
        from tests.test_conf import IP_ADDRESS, PORT, USERNAME, PASSWORD
        ip_address = IP_ADDRESS
        port = PORT
        username = USERNAME
        password = PASSWORD
    except ImportError as e:
        raise e


if __name__ == '__main__':
    
    mailclient = MailClient(ip_address, port, username, password)
    snres_json = mailclient.spam_action()
