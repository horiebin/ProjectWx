# -*- coding: utf-8 -*-
# filename: handle.py
import web
import xml.etree.ElementTree as ET
from dao.user_belong import UserBelongDao
from dao.shop_setting import ShopSettingDao
from util.wx_algorithms import *
import sys
class Handle(object):
    def POST(self):
        data = web.data()
        if len(data) == 0:
            return 'hello, this is handle view'
            print "nothing received"
        else:
            print data
            try:
                xml = ET.fromstring(data)
                msgType = xml.find('MsgType').text
                if msgType == 'event':
                    toUserName = xml.find('ToUserName').text
                    fromUserName = xml.find('FromUserName').text
                    createTime = xml.find('CreateTime').text
                    Event = xml.find('Event').text
                    if Event != 'subscribe' and Event != 'SCAN':
                        reply = 'hello wx'
                    if Event == 'subscribe':
                        EventKey = xml.find('EventKey').text.split('|')[0]
                        shop_id = int(EventKey[8:])
                        rlyContent = '回复0获取贴膜教学\n\n回复1获取产品介绍\n\n领取红包请到淘宝确认收货，进行全五星评价之后点击菜单中的“返现售后”-"五星好评返现"，按照要求提交好评截图跟订单号领取红包\n\n售后问题请联系淘宝客服，本微信只发送红包，不负责任何售后问题。'
                        reply = '''
                                                <xml>
                                                <ToUserName><![CDATA[%s]]></ToUserName>
                                                <FromUserName><![CDATA[%s]]></FromUserName>
                                                <CreateTime>%s</CreateTime>
                                                <MsgType><![CDATA[%s]]></MsgType>
                                                <Content><![CDATA[%s]]></Content>
                                                </xml>
                                                ''' % (
                            fromUserName,
                            toUserName,
                            createTime,
                            'text',
                            rlyContent
                        )
                    if Event == 'SCAN':
                        EventKey = xml.find('EventKey').text
                        shop_id = int(EventKey)
                    shopSetting = ShopSettingDao().getSetting(shop_id)
                    FromUserName = xml.find('FromUserName').text
                    open_id = FromUserName
                    # add user to db
                    UserBelongDao().insertOnUpdate(open_id,shop_id)
                    tags = getUserTags(open_id)
                    for tag in tags:
                        deleteUserTag(open_id,tag)
                    # add tag to wx
                    addShopTagToUser(open_id,shopSetting['wx_tag_id'])
                    return reply
                elif msgType == 'text'or msgType == 'image':
                    toUserName=xml.find('ToUserName').text
                    fromUserName = xml.find('FromUserName').text
                    createTime = xml.find('CreateTime').text
                    messageContent = xml.find('Content').text
                    if messageContent == '0':
                        reply =  '''
                        <xml>
                        <ToUserName><![CDATA[%s]]></ToUserName>
                        <FromUserName><![CDATA[%s]]></FromUserName>
                        <CreateTime>%s</CreateTime>
                        <MsgType><![CDATA[news]]></MsgType>
                        <ArticleCount>4</ArticleCount>
                        <Articles>
                        <item>
                        <Title><![CDATA[贴膜图文教学]]></Title>
                        <Description><![CDATA[贴膜图文教学]]></Description>
                        <PicUrl><![CDATA[http://mmbiz.qpic.cn/mmbiz_jpg/YlHBg1sQElsgUDmlLo78VspngyowyBWEQC0DTp2A9nbh2P1wic0X7yBarq8V8b4TwVA4zrDpuRXZqvyjvXqfJbg/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1]]></PicUrl>
                        <Url><![CDATA[https://mp.weixin.qq.com/s?__biz=MzIzMjEwMjEzMg==&mid=500552511&idx=1&sn=7d4bdf9f44579308458871cf58e831e4&chksm=70bb72a447ccfbb2b75731f8a52df43aa7b73c0713a4d4cff4f1051b8c1967d2ba0c1940b1bb#rd]]></Url>
                        </item>
                        <item>
                        <Title><![CDATA[手机后膜贴膜教程]]></Title>
                        <Description><![CDATA[手机后膜贴膜教程]]></Description>
                        <PicUrl><![CDATA[http://mmbiz.qpic.cn/mmbiz_jpg/YlHBg1sQElsAy2Pw5icfzVaG2XrkCIP30vh80R8oFmG4LxNdgFEkibLuWHYqWUFFWKzwNjOVLUkpIessejNQNoFg/640?tp=webp&wxfrom=5&wx_lazy=1]]></PicUrl>
                        <Url><![CDATA[https://mp.weixin.qq.com/s?__biz=MzIzMjEwMjEzMg==&mid=500552502&idx=1&sn=e6a9d584080615be1e20e07a4c173239&chksm=70bb72ad47ccfbbb34f39a9cdbdd7eb7efde7e7386c563ea4423ee3ad34d700423ea11288252#rd]]></Url>
                        </item>
                        <item>
                        <Title><![CDATA[气泡修复方法]]></Title>
                        <Description><![CDATA[贴膜之后有气泡去除]]></Description>
                        <PicUrl><![CDATA[http://mmbiz.qpic.cn/mmbiz_jpg/mWiccvpqz2XwHIgFVhYBNJ2fUxG0gCU8ey8RtAccW2995jrPWp97qNDVpCY51OY4F2iadK71kfnn0RYmCibVMXrQA/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1]]></PicUrl>
                        <Url><![CDATA[http://mp.weixin.qq.com/s?__biz=MzIzMjEwMjEzMg==&mid=500552499&idx=1&sn=3627d46f49a3712428f3279cd9e805d7&chksm=70bb72a847ccfbbe44072d69a12fb8479c4b131648975c055cf98b582a68f9baaee0b01a3c62#rd]]></Url>
                        </item>
                        <item>
                        <Title><![CDATA[白边处理办法]]></Title>
                        <Description><![CDATA[白边处理]]></Description>
                        <PicUrl><![CDATA[http://mmbiz.qpic.cn/mmbiz_jpg/mWiccvpqz2XwHIgFVhYBNJ2fUxG0gCU8e4FTPauN6wtolQq3eh7hFlWhrvZQKX2vxQf0NzsKu5CNdrVxBrUP70w/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1]]></PicUrl>
                        <Url><![CDATA[https://mp.weixin.qq.com/s?__biz=MzIzMjEwMjEzMg==&mid=500552505&idx=1&sn=a00358e5b670c438e3ce8761a1f1fde4&chksm=70bb72a247ccfbb4cde924f6231d556855164e52e59d203d548c39bd8270f9a59e7dfed3ade5#rd]]></Url>
                        </item>
                        </Articles>
                        </xml>
                        '''%(
                        fromUserName,
                        toUserName,
                        createTime
                        )
                        return reply
                    elif messageContent == '1':
                        reply ='''
                        <xml>
                        <ToUserName><![CDATA[%s]]></ToUserName>
                        <FromUserName><![CDATA[%s]]></FromUserName>
                        <CreateTime>%s</CreateTime>
                        <MsgType><![CDATA[news]]></MsgType>
                        <ArticleCount>5</ArticleCount>
                        <Articles>
                        <item>
                        <Title><![CDATA[丝印全屏膜]]></Title>
                        <Description><![CDATA[全屏膜]]></Description>
                        <PicUrl><![CDATA[http://mmbiz.qpic.cn/mmbiz_jpg/mWiccvpqz2XzNhEsRFlwehQukxI7FRKgxfKMu6bJnDiaUKjWFpmUIpWupWjcWDVZZEuibuFnwlOjr7JNxlmwQpic4g/640?tp=webp&wxfrom=5&wx_lazy=1]]></PicUrl>
                        <Url><![CDATA[http://mp.weixin.qq.com/s?__biz=MzIzMjEwMjEzMg==&mid=500552520&idx=1&sn=4d6eeee9a9db076bd98b4a2c515da6f1&chksm=70bb72d347ccfbc560f058fa17d5108c08c3c63bdabcc7ef7d401ff3ec35179d4ffc260c0436#rd]]></Url>
                        </item>
                        <item>
                        <Title><![CDATA[护眼抗蓝光膜]]></Title>
                        <Description><![CDATA[description]]></Description>
                        <PicUrl><![CDATA[http://mmbiz.qpic.cn/mmbiz_jpg/mWiccvpqz2XzNhEsRFlwehQukxI7FRKgxF0C1JaJ1e4jnwqysDtaOqxaS00W3jv2DmEQ19IHZ7h4tMq9KeJYX0w/640?tp=webp&wxfrom=5&wx_lazy=1]]></PicUrl>
                        <Url><![CDATA[http://mp.weixin.qq.com/s?__biz=MzIzMjEwMjEzMg==&mid=500552519&idx=1&sn=43c06e5ffbde1846e787aec503e80949&chksm=70bb72dc47ccfbca24892634a9bba75a96136eb14d65bbc55554f1cb6816d9053f4cfd3dc8d6#rd]]></Url>
                        </item>
                        <item>
                        <Title><![CDATA[软边钢化膜]]></Title>
                        <Description><![CDATA[软边钢化膜]]></Description>
                        <PicUrl><![CDATA[http://mmbiz.qpic.cn/mmbiz_jpg/mWiccvpqz2XzNhEsRFlwehQukxI7FRKgxKAqBFGdj1z0V7mGs1C2sZPEhHphFicQ4ibpVNIst8jtj7xCdPyicgE7Fg/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1]]></PicUrl>
                        <Url><![CDATA[http://mp.weixin.qq.com/s?__biz=MzIzMjEwMjEzMg==&mid=500552514&idx=1&sn=48ba7325c31610b24e2b105371028829&chksm=70bb72d947ccfbcfc1c6360ca2e4e73872b76b1c78534224311a3452a8908898e839dd44b2ed#rd]]></Url>
                        </item>
                        <item>
                        <Title><![CDATA[非全屏钢化膜]]></Title>
                        <Description><![CDATA[非全屏]]></Description>
                        <PicUrl><![CDATA[http://mmbiz.qpic.cn/mmbiz_jpg/mWiccvpqz2XzNhEsRFlwehQukxI7FRKgxArH9tCwKUfib0aEnz0QqJCUz0iavZcAvngX5M4hFmvslGBApUoWhlNCg/640?tp=webp&wxfrom=5&wx_lazy=1]]></PicUrl>
                        <Url><![CDATA[http://mp.weixin.qq.com/s?__biz=MzIzMjEwMjEzMg==&mid=500552523&idx=1&sn=40aacdfe149cc41529541d75ad54302b&chksm=70bb72d047ccfbc67623d440ad39d54b7896a930669fb7e27d9f2c97225b8ab90e5ce6e1a97e#rd]]></Url>
                        </item>
                        <item>
                        <Title><![CDATA[碳纤维后膜]]></Title>
                        <Description><![CDATA[碳纤维后膜]]></Description>
                        <PicUrl><![CDATA[http://mmbiz.qpic.cn/mmbiz_jpg/mWiccvpqz2XwHIgFVhYBNJ2fUxG0gCU8elrRCveLD65NmOYZXwsz0gG9Pfgw7ytR3D8b5cUzSZPZkgic38tm5wtQ/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1]]></PicUrl>
                        <Url><![CDATA[http://mp.weixin.qq.com/s?__biz=MzIzMjEwMjEzMg==&mid=500552528&idx=1&sn=10f2678cece4bee4d5a1646788d21b7f&chksm=70bb72cb47ccfbdd1f9621b734adfa91f583087d54e116c067fc857a1cb1d9545c282bec129c#rd]]></Url>
                        </item>
                        </Articles>
                        </xml>
                        '''%(
                        fromUserName,
                        toUserName,
                        createTime
                        )
                        return reply
                    elif u'订单' in messageContent:
                        rlyContent = '淘宝确认收货后，在“我的淘宝”，“我的订单”，选择对应的定点，点进去之后，可以一键复制订单号'
                        reply = '''
                        <xml>
                        <ToUserName><![CDATA[%s]]></ToUserName>
                        <FromUserName><![CDATA[%s]]></FromUserName>
                        <CreateTime>%s</CreateTime>
                        <MsgType><![CDATA[%s]]></MsgType>
                        <Content><![CDATA[%s]]></Content>
                        </xml>
                        ''' % (
                        fromUserName,
                        toUserName,
                        createTime,
                        'text',
                        rlyContent
                        )
                        return reply
                    else:
                        rlyContent = '回复0获取贴膜教学\n\n回复1获取产品介绍\n\n领取红包请到淘宝确认收货，进行全五星评价之后点击菜单中的“返现售后”-"五星好评返现"，按照要求提交好评截图跟订单号领取红包\n\n售后问题请联系淘宝客服，本微信只发送红包，不负责任何售后问题。'
                        reply = '''
                        <xml>
                        <ToUserName><![CDATA[%s]]></ToUserName>
                        <FromUserName><![CDATA[%s]]></FromUserName>
                        <CreateTime>%s</CreateTime>
                        <MsgType><![CDATA[%s]]></MsgType>
                        <Content><![CDATA[%s]]></Content>
                        </xml>
                        '''%(
                        fromUserName,
                        toUserName,
                        createTime,
                        'text',
                        rlyContent
                        )
                        return reply
            except:
                    print "Unexpected error:", sys.exc_info()[0]

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
