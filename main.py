# -*- coding: utf-8 -*-
# filename: main.py
import socket

import web

import config
from controller.handle import Handle
from controller.re_fund import Refund
from controller.re_fund import RefundSubmit
from controller.re_fund import RefundHistory
from controller.verify import Verify


urls = (
    '/wx', 'Handle',
    '/MP_verify_0m8uEfoC4BBB1dLi.txt', 'MP_verify_pAX8px3b13vFvntk.txt',
    '/refund', 'Refund',
    '/refund/submit', 'RefundSubmit',
    '/refund/history', 'RefundHistory',
)

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
