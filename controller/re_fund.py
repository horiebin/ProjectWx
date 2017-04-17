import web
from dao.server_config import ServerConfigDao
from util.wx_algorithms import *
import time
from config import Config
from dao.user_upload import UserUploadDao
from dao.verify_refund import VerifyRefundDao
import json

render = web.template.render('templates/')

class Refund:
    def GET(self):
        appId = ServerConfigDao().getAppId()
        jsapi_token = ServerConfigDao().get_jsapi_ticket()
        noncestr = id_generator()
        timestamp = int(time.time())
        url = web.ctx.home + web.ctx.fullpath
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
        unVerifyRecords = userUploadDao.selectByOpenId(shopId,openId)
        verifyRefundDao = VerifyRefundDao()
        verifyRecords = verifyRefundDao.selectByOpenId(shopId,openId)
        return render.history(unVerifyRecords,verifyRecords)

class RefundOauth():
    def GET(self):
        data = web.input()
        shopid = data.shopid
        oauth2('/refund','snsapi_base',shopid)
