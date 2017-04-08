# -*- coding: utf-8 -*-
# filename: main.py
import web
import socket
import config
from handle import Handle
from re_fund import Refund
urls = (
    '/wx', 'Handle',
    '/refund', 'Refund',
)

if __name__ == '__main__':
    myname = socket.getfqdn(socket.gethostname())
    if myname == 'iZ94mm9cb9hZ':
        print('server is running on %s ...'% myname)
        config.config = config.config_server

    app = web.application(urls, globals())
    app.run()
