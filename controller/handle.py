# -*- coding: utf-8 -*-
# filename: handle.py
from django.http import HttpRequest
import hashlib
import web
import xml.etree.ElementTree as ET
from dao.user_belong import UserBelongDao

import sys
class Handle(object):
    def POST(self):
        data = web.data()
        if len(data) == 0:
            return 'hello, this is handle view'
            print "nothing received"
        else:
            try:
                xml = ET.fromstring(data)
                Event = xml.find('Event').text[9:-2]
                if Event != 'subscribe':
                    return 'hello wx'
                EventKey = xml.find('EventKey').text[9:-2]
                shop_id = int(EventKey)
                FromUserName = xml.find('FromUserName').text[9:-2]
                open_id = FromUserName
                UserBelongDao().insertOnUpdate(open_id,shop_id)
            except :
                print "Unexpected error:", sys.exc_info()[0]
            sys.stdout.flush()
    def GET(self): 
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "huson&horiebin" #请按照公众平台官网\基本配置中信息填写

            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            print "handle/GET func: hashcode, signature: ", hashcode, signature
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception, Argument:
            return Argument
