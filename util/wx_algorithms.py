import string
import random
import hashlib
from config import Config
from dao.server_config import ServerConfigDao
from dao.mp_info import MpInfoDao
import web
import urllib3
import json
import warnings
from dao.admin_config import AdminConfigDao
warnings.filterwarnings("ignore")

http = urllib3.PoolManager()

def id_generator(size=16, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def js_signature(noncestr,jsapi_ticket,timestamp,url):
    s = "jsapi_ticket=%s&noncestr=%s&timestamp=%d&url=%s" %(jsapi_ticket,
                                                              noncestr,timestamp,url)
    h = hashlib.sha1(s)
    return h.hexdigest()

def oauth2(redictUrl,scope,state,namespace):
    redictUrl = r'http://' + ServerConfigDao()['domin_name'] + redictUrl
    if namespace.isdigit():
        mp = MpInfoDao().getSettingById(namespace)
        component_appid = AdminConfigDao().getValue('admin','app_id')
        appId = mp.authorizer_appid
        target = r'https://open.weixin.qq.com/connect/oauth2/authorize?' \
              r'appid=%s&redirect_uri=%s&response_type=code&scope=%s&state=%s&component_appid=%s' \
              r'#wechat_redirect' %(appId,redictUrl,scope,state,component_appid)
    else:
        appId = ServerConfigDao().getValue(namespace,'app_id')
        target = r'https://open.weixin.qq.com/connect/oauth2/authorize?' \
                 r'appid=%s&redirect_uri=%s&response_type=code&scope=%s&state=%s&connect_redirect=1#' \
                 r'wechat_redirect' % (appId, redictUrl, scope, state)
    #print target
    raise web.seeother(target)

def getOpenIdByCode(code,namespace):
    if namespace.isdigit():
        mp = MpInfoDao().getSettingById(namespace)
        appId = mp.authorizer_appid
        component_appid = AdminConfigDao().getValue('admin', 'app_id')
        component_access_token = AdminConfigDao().getValue('admin','component_access_token')
        url = r'https://api.weixin.qq.com/sns/oauth2/component/access_token?' \
              r'appid=%s&code=%s&grant_type=authorization_code&component_appid=%s' \
              r'&component_access_token=%s' %(appId,code,component_appid,component_access_token)
    else:
        appId = ServerConfigDao().getValue(namespace,'app_id')
        secret = ServerConfigDao().getValue(namespace,'app_secret')
        url = r'https://api.weixin.qq.com/sns/oauth2/access_token?' \
              r'appid=%s&secret=%s&code=%s&grant_type=authorization_code'%(appId,secret,code)
    r = http.request('GET',url)
    urlResp = json.loads(r.data)
    if 'openid' not in urlResp:
        print r.data
    return urlResp['openid']

def addShopTagToUser(open_id,shop_tag_id,namespace):
    accessToken = ServerConfigDao().getValue(namespace,'access_token')
    target = r'https://api.weixin.qq.com/cgi-bin/tags/members/batchtagging?access_token=%s' % accessToken
    data = {'openid_list':[open_id],'tagid':shop_tag_id}
    payload = json.dumps(data)
    s = http.request('POST',target,body=payload)
    res = json.loads(s.data)
    if res['errcode'] != 0:
        print 'adding tag error:', s.text

def getUserTags(open_id,namespace):
    accessToken = ServerConfigDao().getValue(namespace,'access_token')
    target = r'https://api.weixin.qq.com/cgi-bin/tags/getidlist?access_token=%s' %accessToken
    data = {'openid':open_id}
    payload = json.dumps(data)
    s = http.request('POST',target,body=payload)
    res = json.loads(s.data)
    if 'tagid_list' not in res:
        print s.data
    tags = res['tagid_list']
    return tags


def deleteUserTag(open_id,tag,namespace):
    accessToken = ServerConfigDao().getValue(namespace,'access_token')
    target = r'https://api.weixin.qq.com/cgi-bin/tags/members/batchuntagging?access_token=%s' %accessToken
    data = {'openid_list':[open_id],'tagid':tag}
    payload = json.dumps(data)
    s = http.request('POST',target,body=payload)
    res = json.loads(s.data)
    if res['errcode'] != 0:
        print 'adding tag error:', s.text

def createTag(name,namespace):
    accessToken = ServerConfigDao().getValue(namespace,'access_token')
    target = r'https://api.weixin.qq.com/cgi-bin/tags/create?access_token=%s' %accessToken
    data = {'tag':{'name':name}}
    payload = json.dumps(data)
    s = http.request('POST',target,body=payload)
    res = json.loads(s.data)
    return res['tag']['id']
