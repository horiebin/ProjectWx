import web
from dao.server_config import ServerConfig
from util.wx_algorithms import *
import time
from config import config

render = web.template.render('templates/')

class Refund:
    def GET(self):
        sc = ServerConfig()
        appId = config['appId']
        jsapi_token = sc.get_jsapi_ticket()
        noncestr = id_generator()
        timestamp = int(time.time())
        url = r'http://' + config['host'] + r'/refund'
        sign = js_signature(noncestr,jsapi_token,timestamp,url)
        return render.refund(appId,sign,noncestr,timestamp)