# -*- coding: utf-8 -*-
# filename: main.py
import socket

import web

from util.log import Log
import config
from controller.handle import Handle
from controller.re_fund import Refund
from controller.re_fund import RefundSubmit
from controller.re_fund import RefundHistory
from controller.re_fund import RefundOauth
from controller.verify import VerifyXwpay
from controller.verify import VerifyGZChenlan

from controller.cross_refund import *
import sys 

reload(sys)
sys.setdefaultencoding('utf8')
web.config.debug = True#config.debug

urls = (
    '/wx', 'Handle',
    '/MP_verify_xHfVRSc4XZjB8oTQ.txt', 'VerifyXwpay',
    '/MP_verify_7DY5qAd936DYwWrL.txt', 'VerifyGZChenlan',

    '/cross_refund/oauth1', 'Oauth1',
    '/cross_refund/cross', 'Cross',
    '/cross_refund/oauth2', 'Oauth2',
    '/cross_refund/page', 'CrossRefundPage',
    '/cross_refund/submit', 'CrossRefundSubmit',
    '/cross_refund/history', 'CrossRefundHistory',
)
app = web.application(urls, globals())
if not config.debug :
    app = app.wsgifunc(Log)

# def session_hook():
#     web.ctx.session = session


if __name__ == '__main__':
    app.run(Log)

