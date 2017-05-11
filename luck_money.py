from util.wx_algorithms import *
from dicttoxml import dicttoxml
import requests
from dao.server_config import ServerConfigDao


def sendLuckyMoney(open_id,order_id,amount,mch_id,appid,send_name,pay_key):
    nonce_str = id_generator()
    mch_billno = order_id
    mch_id = mch_id
    wxappid = appid
    send_name = send_name
    re_openid = open_id
    total_amount = amount
    total_num = 1
    wishing = 'bestwishes'
    client_ip = '120.25.195.197'
    act_name = 'refund'
    remark = '1'

    data = {'nonce_str':nonce_str,'mch_billno':mch_billno,'mch_id':mch_id,'wxappid':wxappid,
            'send_name':send_name,'re_openid':re_openid,'total_amount':total_amount,
            'total_num':total_num,'wishing':wishing,'client_ip':client_ip,'act_name':act_name,
            'remark':remark}

    stringA = ''
    for key in sorted(data):
        stringA += key + '=' + str(data[key]) + '&'
    stringA = stringA[:-1]
    stringSignTemp = stringA + "&key="+pay_key

    print stringSignTemp
    h = hashlib.md5(stringSignTemp)
    sign = h.hexdigest().upper()
    data['sign'] = sign
    xml = dicttoxml(data, custom_root='xml', attr_type=False)
    print xml
    url = r'https://api.mch.weixin.qq.com/mmpaymkttransfers/sendredpack'
    s = requests.post(url=url,data=xml)
    print s.text

if __name__ == '__main__':
    payKey = ServerConfigDao()['pay_key']
    payId = ServerConfigDao()['pay_id']
    appid = ServerConfigDao()['app_id']
    sendLuckyMoney('o9PalwGfi1ZuofhVfXu6JOMKAFUo','6543697412365412',1,payId,appid,'huson',payKey)