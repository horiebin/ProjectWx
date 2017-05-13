import web
from dao.server_config import ServerConfigDao
from util.wx_algorithms import *
import time
from config import Config
from dao.user_upload import UserUploadDao
from dao.verify_refund import VerifyRefundDao
from dao.order_ids import OrderIdsDao
from dao.shop_setting import ShopSettingDao
from dao.log_change_money import LogShopMoneyDao
from dao.shop_account import ShopAccountDao
import json

render = web.template.render('templates/')

class Refund:
    def GET(self):
        appId = ServerConfigDao().getAppId()
        jsapi_token = ServerConfigDao().get_jsapi_ticket()
        noncestr = id_generator()
        timestamp = int(time.time())
        url = r'http://'+Config()['server'] + web.ctx.fullpath
        sign = js_signature(noncestr,jsapi_token,timestamp,url)
        data = web.input()
        code = data.code
        shopid = data.state
        openid = getOpenIdByCode(code)
        return render.refund(appId,sign,noncestr,timestamp,shopid,openid)

class RefundSubmit:
    def POST(self):
        data = web.input()
        if len(data) == 0:
            return 'Hello, this is submit'

        data = json.loads(data.info);
        serverIds = data['server_ids']
        orderId = data['order_id']
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
        oauth2('/refund','snsapi_base',shopid)
