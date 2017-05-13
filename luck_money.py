# -*- coding: utf-8 -*-
from util.wx_algorithms import *
from dicttoxml import dicttoxml
import requests
from dao.server_config import ServerConfigDao
from dao.verify_refund import VerifyRefundDao
from dao.shop_setting import ShopSettingDao
import xml.etree.ElementTree as ET
from md5 import md5

def sign(params,pay_key):
    '''
    https://pay.weixin.qq.com/wiki/doc/api/tools/cash_coupon.php?chapter=4_3
    '''
    params = [(str(key), str(val)) for key, val in params.iteritems() if val]
    sorted_params_string = '&'.join('='.join(pair) for pair in sorted(params))
    sign = '{}&key={}'.format(sorted_params_string, pay_key)
    return md5(sign).hexdigest().upper()

def sendLuckyMoney(open_id,order_id,amount,mch_id,appid,send_name,pay_key):
    nonce_str = id_generator()
    mch_billno = order_id
    mch_id = mch_id
    wxappid = appid
    send_name = send_name
    re_openid = open_id
    total_amount = amount
    total_num = '1'
    wishing = u'感谢您的好评'
    client_ip = '120.25.195.197'
    act_name = u'红包返现'
    remark = '1'

    data = {'nonce_str':nonce_str,'mch_billno':mch_billno,'mch_id':mch_id,'wxappid':wxappid,
            'send_name':send_name,'re_openid':re_openid,'total_amount':total_amount,
            'total_num':total_num,'wishing':wishing,'client_ip':client_ip,'act_name':act_name,
            'remark':remark}

    #data = {'nonce_str':nonce_str,'mch_billno':mch_billno,'mch_id':mch_id,'wxappid':wxappid,
    #        're_openid':re_openid,'total_amount':total_amount,
    #        'total_num':total_num,'client_ip':client_ip,
    #        'remark':remark}

    stringA = ''
    for key in sorted(data):
        stringA += key + '=' + data[key] + '&'
    stringA = stringA[:-1]
    stringSignTemp = stringA + "&key="+pay_key

    print stringSignTemp
    h = hashlib.md5(stringSignTemp.encode('utf-8'))
    sign = h.hexdigest().upper()
    print sign
    # sign_str = sign(data,pay_key)
    #data['wishing'] = wishing
    #data['act_name'] = act_name
    #data['send_name'] =send_name
    data['sign'] = sign
    xml = dicttoxml(data, custom_root='xml', attr_type=False)
    print xml
    url = r'https://api.mch.weixin.qq.com/mmpaymkttransfers/sendredpack'
    s = requests.post(url=url,data=xml,cert=("../pems/apiclient_cert.pem","../pems/apiclient_key.pem"))
    xml = ET.fromstring(s.text.encode('utf-8'))
    code = xml.find('result_code').text
    if code == 'SUCCESS':
        print s.text
        return True
    else:
        print s.text
        return False


if __name__ == '__main__':
    payKey = ServerConfigDao()['pay_key']
    payId = ServerConfigDao()['pay_id']
    appid = ServerConfigDao()['app_id']
    shopIdtoName = {}

    while True:
        rows = VerifyRefundDao().selectByPage(100)
        if len(rows) == 0:
            break
        for row in rows:
            if row['shop_id'] not in shopIdtoName:
                shopSetting = ShopSettingDao().getSetting(row['shop_id'])
                shopIdtoName[row['shop_id']] = shopSetting['name']
            shop_name = shopIdtoName[row['shop_id']]
            order_id = row['order_id']
            open_id = row['open_id']
            result = sendLuckyMoney(open_id,order_id,str(row['money']),payId,appid,shop_name,payKey)
            if result :
                VerifyRefundDao().setRefundFlag(row['id'])
