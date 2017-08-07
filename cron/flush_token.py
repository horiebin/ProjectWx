import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from dao.server_config import ServerConfigDao
from basic import Basic
import urllib
import requests
import json

def flush_config_task():

    print('----start reflesh token----')
    names = ServerConfigDao().getAllNamespace()
    for name in names:
        flush_token_name(name)

def flush_token_name(name):
    appId = ServerConfigDao().getValue(name, 'app_id')
    appSecret = ServerConfigDao().getValue(name, 'app_secret')

    postUrl = ("https://api.weixin.qq.com/cgi-bin/token?grant_type="
               "client_credential&appid=%s&secret=%s" % (appId, appSecret))
    urlResp = urllib.urlopen(postUrl)
    urlResp = json.loads(urlResp.read())

    accessToken = urlResp['access_token']
    ServerConfigDao().setValue(name, 'access_token', accessToken)

    url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket'
    payload = {'access_token': accessToken, 'type': 'jsapi'}
    resp = requests.get(url, params=payload)
    r = json.loads(resp.content)
    ticket = r['ticket']
    ServerConfigDao().setValue(name, 'jsapi_ticket', ticket)

if __name__ == "__main__":
    flush_config_task()
