# -*- coding: utf-8 -*-

import web
from dao.server_config import ServerConfigDao
from util.wx_algorithms import *
import time
import config
from dao.user_upload import UserUploadDao
from dao.verify_refund import VerifyRefundDao
from dao.order_ids import OrderIdsDao
from dao.shop_setting import ShopSettingDao
from dao.log_change_money import LogShopMoneyDao
from dao.shop_account import ShopAccountDao
from dao.user_belong import UserBelongDao
from dao.openid_match import OpenidMatch
import json

render = web.template.render('templates/')


class Refund:
    def __init__(self, ):
        self.logger = web.ctx.env.get('wsgilog.logger')
        self.logger.info("log test")

    def GET(self):
        data = web.input()
        code = data.code
        namespace = data.state

        openid = getOpenIdByCode(code)
        if not namespace:
            return u'请重新点击链接'
        OpenidMatch().insertSourceUser(openid,namespace) #finish first redirect

        target = r'/pay_refund_oauth?openid=%s'%openid
        raise web.seeother(target)

        return render.refund(appId,sign,noncestr,timestamp,shopid,openid)

class RefundPay:
    def GET(self):
        data = web.input()
        code = data.code
        source_openid = data.state
        openid = getOpenIdByCode(code)
        if not source_openid:
            return u'请重新点击链接'

        OpenidMatch().insertPayUser(openid,source_openid)
        namespace = config.pay_namespace
        appId = ServerConfigDao().getValue(namespace,'app_id')
        jsapi_token = ServerConfigDao().getValue(namespace,'jsapi_token')
        noncestr = id_generator()
        timestamp = int(time.time())
        url = r'http://'+ServerConfigDao()['domin_name'] + web.ctx.fullpath
        sign = js_signature(noncestr,jsapi_token,timestamp,url)

        return render.refund(appId,sign,noncestr,timestamp,namespace,openid)

class RefundSubmit:
    def POST(self):
        data = web.input()
        if len(data) == 0:
            return 'Hello, this is submit'

        data = json.loads(data.info);
        serverIds = data['server_ids']
        orderId = data['order_id'].replace(' ','')
        shopId = data['shop_id']
        openId = data['open_id']
        userUploadDao = UserUploadDao()

        shopSetting = ShopSettingDao().getSetting(shopid=shopId)
        if shopSetting['filter_orderid_flag'] == 1:
            # open filter function
            if not OrderIdsDao().verifyByOrderID(orderId):
                return 'wrong'
        auto_pass = shopSetting['auto_pass_flag']
        if auto_pass == 1:
            #check money is enough
            money = LogShopMoneyDao().getMoneyByShopId(shopid=shopId)
            effectRows = ShopAccountDao().reduceMoney(shopid=shopId,money=money)
            
            if effectRows >0:
                # only save basic information
                res = userUploadDao.insertAutoPass(shopId, openId, orderId)
                if res:
                    # save pass record in another table
                    VerifyRefundDao().insertVerifyRefund(shopId,openId,orderId,money)
                    return 'true'
                else:
                    #add money back
                    ShopAccountDao().addbackMoney(shopId,money)
                    return 'false'
            else: # not enough money, can't auto pass
                auto_pass = 0
        if auto_pass == 0:
            if len(serverIds) == 0:
                res = userUploadDao.insert(shopId,openId, orderId)
            elif len(serverIds) == 1:
                res = userUploadDao.insert(shopId,openId, orderId, serverIds[0])
            elif len(serverIds) == 2:
                res = userUploadDao.insert(shopId,openId, orderId, serverIds[0], serverIds[1])
            else:
                res = userUploadDao.insert(shopId,openId, orderId, serverIds[0], serverIds[1], serverIds[2])

        if res:
            return 'true'
        else:
            return 'false'

class RefundHistory():
    def GET(self):
        data = web.input()
        openId = data.openId
        shopId = data.shopId
        userUploadDao = UserUploadDao()
        uploads = userUploadDao.selectByOpenId(shopId,openId)
        return render.history(uploads)

class RefundOauth():
    def GET(self):
        data = web.input()
        shopid = data.shopid
        namespace = ShopSettingDao().getSetting(shopid)['namespace']
        oauth2('/refund','snsapi_base',namespace,namespace)

class PayRefundOauth():
    def GET(self):
        data = web.input()
        source_openid = data.openid
        namespace = config.pay_namespace
        oauth2('/refund/pay', 'snsapi_base', source_openid, namespace)