import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from dao.server_config import ServerConfigDao
from basic import Basic
import requests
import json

def flush_config_task():

    sc = ServerConfigDao()
    print('----start reflesh token----')
    accessToken = Basic().get_access_token()
    print(accessToken)
    sc.set_access_token(accessToken)

    print('----start reflesh jsapi_ticket')
    url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket'
    payload = {'access_token': accessToken, 'type': 'jsapi'}
    resp = requests.get(url, params=payload)
    r = json.loads(resp.content)
    ticket = r['ticket']
    print(ticket)
    sc.set_jsapi_ticket(ticket)

if __name__ == "__main__":
    flush_config_task()
