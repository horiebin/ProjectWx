import web
from dao.server_config import ServerConfigDao
from util.wx_algorithms import *
import time
from config import Config
from dao.user_upload import UserUploadDao
import json

render = web.template.render('templates/')

class Refund:
    def GET(self):
        sc = ServerConfigDao()
        config = Config()
        appId = config['appId']
        jsapi_token = sc.get_jsapi_ticket()
        noncestr = id_generator()
        timestamp = int(time.time())
        url = r'http://' + config['server'] + r'/refund'
        sign = js_signature(noncestr,jsapi_token,timestamp,url)
        return render.refund(appId,sign,noncestr,timestamp)

class RefundSubmit:
    def POST(self):
        data = web.input()
        if len(data) == 0:
            return 'Hello, this is submit'
        data = json.loads(data.info);
        serverIds = data['server_ids']
        orderId = data['order_id']

        userUploadDao = UserUploadDao()
        if len(serverIds) == 0:
            userUploadDao.insert(0, orderId);
        elif len(serverIds) == 1:
            userUploadDao.insert(0, orderId, serverIds[0])
        elif len(serverIds) == 2:
            userUploadDao.insert(0, orderId, serverIds[0], serverIds[1])
        else:
            userUploadDao.insert(0, orderId, serverIds[0], serverIds[1], serverIds[2])

