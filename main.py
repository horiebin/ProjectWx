# -*- coding: utf-8 -*-
# filename: main.py
import web
from handle import Handle
from re_fund import Refund
urls = (
    '/wx', 'Handle',
    '/refund', 'Refund',
)

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
