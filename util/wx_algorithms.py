import string
import random
import hashlib
from config import Config
from dao.server_config import ServerConfigDao
import web
import urllib
import json

def id_generator(size=16, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def js_signature(noncestr,jsapi_ticket,timestamp,url):
    s = "jsapi_ticket=%s&noncestr=%s&timestamp=%d&url=%s" %(jsapi_ticket,
                                                              noncestr,timestamp,url)
    h = hashlib.sha1(s)
    return h.hexdigest()

def oauth2(redictUrl,scope,state):
    appId = ServerConfigDao().getAppId()
    redictUrl = r'http://' + Config()['server'] + redictUrl
    scope = scope
    state = state
    target = r'https://open.weixin.qq.com/connect/oauth2/authorize?' \
             r'appid=%s&redirect_uri=%s&response_type=code&scope=%s&state=%s#' \
             r'wechat_redirect' % (appId, redictUrl, scope, state)
    raise web.seeother(target)

def getOpenIdByCode(code):
    appId = ServerConfigDao().getAppId()
    secret = ServerConfigDao().getAppSecret()
    url = r'https://api.weixin.qq.com/sns/oauth2/access_token?' \
          r'appid=%s&secret=%s&code=%s&grant_type=authorization_code'%(appId,secret,code)
    urlResp = urllib.urlopen(url)
    urlResp = json.loads(urlResp.read())
    return urlResp['openid']