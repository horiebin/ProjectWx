# -*- coding: utf-8 -*-
# filename: main.py
import socket

import web

from util.log import Log
from controller.handle import Handle
from controller.re_fund import Refund
from controller.re_fund import RefundSubmit
from controller.re_fund import RefundHistory
from controller.re_fund import RefundOauth
from controller.verify import VerifyXwpay
from controller.verify import VerifyGZChenlan


web.config.debug = False

urls = (
    '/wx', 'Handle',
    '/MP_verify_xHfVRSc4XZjB8oTQ.txt', 'VerifyXwpay',
    '/MP_verify_7DY5qAd936DYwWrL.txt', 'VerifyGZChenlan',
    '/refund', 'Refund',
    '/refund/submit', 'RefundSubmit',
    '/refund/history', 'RefundHistory',
    '/refund/oauth','RefundOauth',
)
app = web.application(urls, globals())
app = app.wsgifunc(Log)

# def session_hook():
#     web.ctx.session = session


if __name__ == '__main__':
    app.run(Log)

