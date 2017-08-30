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
from dao.mp_info import MpInfoDao
import numbers
import json

render = web.template.render('templates/')
shop_tag={"105":"10001","104":"10002","106":"10003","110":"10004","111":"10005","112":"10006",
          "113":"10007","114":"10008","115":"10009","116":"10011"}

class Cross:
    def __init__(self, ):
        self.logger = web.ctx.env.get('wsgilog.logger')
        self.logger.info("log test")

    def GET(self):
         #finish first redirect

        target = r'/cross_refund/oauth2?openid=%s'%'openid'
        raise web.seeother(target)

        return render.refund(appId,sign,noncestr,timestamp,shopid,openid)

class CrossRefundPage:
    def GET(self):
        data = web.input()
        print data
        code = data.code
        source_openid = data.state[0:28]
        source_namespace = data.state[28:]

        source_app_id = ServerConfigDao().getValue(source_namespace,'app_id')
        mp_setting = MpInfoDao().getSettingByAppid(source_app_id)
        platform = mp_setting['platform']

        namespace = config.pay_namespace
        openid = getOpenIdByCode(code, namespace)
        OpenidMatch().insertPayUser(openid,source_openid)

        appId = ServerConfigDao().getValue(namespace,'app_id')
        jsapi_token = ServerConfigDao().getValue(namespace,'jsapi_ticket')
        noncestr = id_generator()
        timestamp = int(time.time())
        url = r'http://'+ServerConfigDao()['domin_name'] + web.ctx.fullpath
        sign = js_signature(noncestr,jsapi_token,timestamp,url)

        return render.refund(appId,sign,noncestr,timestamp,openid,platform)

class CrossRefundSubmit:
    def POST(self):
        data = web.input()
        if len(data) == 0:
            return 'Hello, this is submit'

        data = json.loads(data.info)
        serverIds = data['server_ids']
        orderId = data['order_id'].replace(' ','')
        openId = data['open_id']
        userUploadDao = UserUploadDao()

        row = OrderIdsDao().verifyByOrderID(orderId)
        if not row:
            return 'wrong'
        shopId = row['shop_id']
        UserBelongDao().insertOnUpdate(openId, shopId)

        shopSetting = ShopSettingDao().getSetting(shopid=shopId)

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

class CrossRefundHistory():
    def GET(self):
        data = web.input()
        openId = data.openId
        shopId = UserBelongDao().getShopIdByOpenId(openId)

        userUploadDao = UserUploadDao()
        uploads = userUploadDao.selectByOpenId(shopId,openId)
        return render.history(uploads)

class Oauth1():
    def GET(self):
        data = web.input()
        namespace = data.name
        oauth2('/cross_refund/oauth2','snsapi_base',namespace,namespace)


class Oauth2():
    def GET(self):
        data = web.input()
        code = data.code
        source_namespace = data.state
        source_openid = getOpenIdByCode(code, source_namespace)
        OpenidMatch().insertSourceUser(source_openid, source_namespace)
        namespace = config.pay_namespace
        oauth2('/cross_refund/page', 'snsapi_base', source_openid + source_namespace , namespace)
