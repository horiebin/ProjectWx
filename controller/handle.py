# -*- coding: utf-8 -*-
# filename: handle.py
import web
import xml.etree.ElementTree as ET
from dao.user_belong import UserBelongDao
from dao.shop_setting import ShopSettingDao
from util.wx_algorithms import *
from dao.auto_reply import AutoReplyDao
from dao.server_config import ServerConfigDao

class Handle(object):
    def __init__(self, ):
        self.logger = web.ctx.env.get('wsgilog.logger')
        self.logger.info("log test")

    def POST(self):
        data = web.data()
        if len(data) == 0:
            return 'hello, this is handle view'
        else:
            xml = ET.fromstring(data)
            namespace = ServerConfigDao().getNameSpaceByOriginalId(xml.find('ToUserName').text)
            msgType = xml.find('MsgType').text
            autoReply = AutoReplyDao().getAllReplys()
            reply = None
            if msgType == 'event':

                Event = xml.find('Event').text
                if Event != 'subscribe' and Event != 'SCAN':
                    return 'hello wx'
                if Event == 'subscribe':
                    EventKey = xml.find('EventKey').text.split('|')[0]
                    shop_id = int(EventKey[8:])
                    reply = autoReply[0]
                if Event == 'SCAN':
                    EventKey = xml.find('EventKey').text
                    shop_id = int(EventKey)
                    reply = autoReply[0]
                shopSetting = ShopSettingDao().getSetting(shop_id)
                FromUserName = xml.find('FromUserName').text
                open_id = FromUserName
                # add user to db
                UserBelongDao().insertOnUpdate(open_id, shop_id)
                tags = getUserTags(open_id,namespace)
                for tag in tags:
                    deleteUserTag(open_id, tag,namespace)
                # add tag to wx
                addShopTagToUser(open_id, shopSetting['wx_tag_id'],namespace)


            elif msgType == 'text':
                messageContent = xml.find('Content').text
                for row in autoReply[1:]:
                    if row['match_type'] == 0:
                        if messageContent == row['match_content']:
                            reply = row
                            break
                    elif row['match_type'] == 1:
                        if row['match_content'] in messageContent :
                            reply = row
                            break
            else:
                for row in autoReply[1:]:
                    if row['match_content'] == 'image':
                        reply = row
                        break

            if reply is not None :
                toUserName = xml.find('ToUserName').text
                fromUserName = xml.find('FromUserName').text
                createTime = xml.find('CreateTime').text

                replyWx = '''
                        <xml>
                        <ToUserName><![CDATA[%s]]></ToUserName>
                        <FromUserName><![CDATA[%s]]></FromUserName>
                        <CreateTime>%s</CreateTime>
                        <MsgType><![CDATA[%s]]></MsgType>
                        %s
                        </xml>
                        '''%(
                        fromUserName,
                        toUserName,
                        createTime,
                        reply['message_type'],
                        reply['reply_content']
                        )
                return replyWx
            else :
                return ''


    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "huson8horiebin" #请按照公众平台官网\基本配置中信息填写

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
