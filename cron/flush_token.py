from dao.server_config import ServerConfigDao
from basic import Basic
import requests
import json

if __name__ == "__main__":
    sc = ServerConfigDao()
    print('----start reflesh token----')
    accessToken = Basic().get_access_token()
    print(accessToken)
    sc.set_access_token(accessToken)

    print('----start reflesh jsapi_ticket')
    url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket'
    payload = {'access_token':accessToken, 'type':'jsapi'}
    resp = requests.get(url,params=payload)
    r = json.loads(resp.content)
    ticket = r['ticket']
    print(ticket)
    sc.set_jsapi_ticket(ticket)
