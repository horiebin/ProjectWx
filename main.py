# -*- coding: utf-8 -*-
# filename: main.py
import socket

import web

import cron.flush_token
from controller.handle import Handle
from controller.re_fund import Refund
from controller.re_fund import RefundSubmit
from controller.re_fund import RefundHistory
from controller.re_fund import RefundOauth
from controller.verify import Verify


urls = (
    '/wx', 'Handle',
    '/MP_verify_pAX8px3b13vFvntk.txt', 'Verify',
    '/refund', 'Refund',
    '/refund/submit', 'RefundSubmit',
    '/refund/history', 'RefundHistory',
    '/refund/oauth','RefundOauth',
)

# def session_hook():
#     web.ctx.session = session


if __name__ == '__main__':
    cron.flush_token.start_flush_timer()
    app = web.application(urls, globals())
    # session = web.session.Session(app, web.session.DiskStore('sessions'),
    #                               initializer={})
    # app.add_processor(web.loadhook(session_hook))
    app.run()

