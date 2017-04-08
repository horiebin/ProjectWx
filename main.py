# -*- coding: utf-8 -*-
# filename: main.py
import socket

import web

import config
from controller.handle import Handle
from controller.re_fund import Refund
from controller.verify import Verify

urls = (
    '/wx', 'Handle',
    '/MP_verify_0m8uEfoC4BBB1dLi.txt', 'Verify',
    '/refund', 'Refund',
)

if __name__ == '__main__':
    myname = socket.getfqdn(socket.gethostname())
    if myname == 'iZ94mm9cb9hZ':
        print('server is running on %s ...'% myname)
        config.config = config.config_server

    app = web.application(urls, globals())
    app.run()
