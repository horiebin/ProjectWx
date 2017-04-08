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
    myaddr = socket.gethostbyname(myname)
    if myaddr == '10.116.10.44':
        config.config = config.config_server

    app = web.application(urls, globals())
    app.run()
