 # -*- coding: utf-8 -*-

from menu import Menu
from basic import Basic

myMenu = Menu()
postJson = """
{
    "button":
    [
        {
            "name": "好评返现",
            "type": "view",
            "url": "http://wx.51dingxiao.com/cross_refund/oauth1?name=kuxiao"
        },
        {
            "name": "产品介绍",
            "sub_button":
            [
                {
                    "type": "view",
                    "name": "非全屏钢化膜",
                    "url": "http://mp.weixin.qq.com/s?__biz=MzA3ODkxMzQ5Mw==&mid=100000045&idx=1&sn=44a2bee18c9fdb8cb41894f05c8c0e56&chksm=1fbacb9728cd4281a82d9e2e15f3b5f2747269cc399f5977d9cf1e5920e9bf4081b5254e1592#rd"
                },
                {
                    "type": "view",
                    "name": "全屏钢化膜",
                    "url": "http://mp.weixin.qq.com/s?__biz=MzA3ODkxMzQ5Mw==&mid=100000039&idx=1&sn=5e15b34b7e0a580b138278c9e893848c&chksm=1fbacb9d28cd428bdeb942f6e3c4d6d214d94200914d7fb0bec02e9c54767ca8e17e9e909c71#rd"
                },
                {
                    "type": "view",
                    "name": "抗蓝光钢化膜",
                    "url": "http://mp.weixin.qq.com/s?__biz=MzA3ODkxMzQ5Mw==&mid=100000048&idx=1&sn=3c723677364d0cb88f77b3e3b944ad98&chksm=1fbacb8a28cd429c4b071316d34da7f73700f97829b1479f7393cefabe8d293a4000236141cd#rd"
                },
                {
                    "type": "view",
                    "name": "3D曲面软边钢化膜",
                    "url": "http://mp.weixin.qq.com/s?__biz=MzA3ODkxMzQ5Mw==&mid=100000042&idx=1&sn=3d18408769a36e1b8cde93af972726d6&chksm=1fbacb9028cd42867b2d8fdd703f7288a1d84e37e93b3ae98991b0f35447cbc476c5c8f2403f#rd"
                }
            ]
        },
        {
            "name": "贴膜教学",
            "sub_button":
            [
                {
                    "type": "view",
                    "name": "贴膜教学",
                    "url": "http://mp.weixin.qq.com/s?__biz=MzA3ODkxMzQ5Mw==&mid=100000050&idx=1&sn=c23aa0447bfef3f906f5ffb4dc9aefe0&chksm=1fbacb8828cd429e74af6131427db12e7e2be77144a22f87d8729009e7e9874cd79c6d421cfe#rd"
                },
                {
                    "type": "view",
                    "name": "白边修复方法",
                    "url": "http://mp.weixin.qq.com/s?__biz=MzA3ODkxMzQ5Mw==&mid=100000030&idx=1&sn=f2dc96f4000a4b9099be8e04fe7d736a&chksm=1fbacba428cd42b2b6c22dbb60d3da78c12c324d4cf34404db0838f67f7669dd23846c482b91#rd"
                },
                {
                    "type": "view",
                    "name": "贴后膜方法",
                    "url": "http://mp.weixin.qq.com/s?__biz=MzA3ODkxMzQ5Mw==&mid=100000027&idx=1&sn=924e4bd625478efb39e72e04d69fc605&chksm=1fbacba128cd42b708f7be016c6e6b7e1ca6117871698de973e37bb0a988a4db9d3bf05d369c#rd"
                },
                {
                    "type": "view",
                    "name": "贴膜后进灰尘修复方法",
                    "url": "http://mp.weixin.qq.com/s?__biz=MzA3ODkxMzQ5Mw==&mid=100000036&idx=1&sn=28f6066d170712a0607bd003743d76c2&chksm=1fbacb9e28cd428844dcdcf3460a25fea97ba3cdbf156562adef8913f36a8660749d819a3239#rd"
                },
                {
                    "type": "view",
                    "name": "贴膜后有气泡修复方法",
                    "url": "http://mp.weixin.qq.com/s?__biz=MzA3ODkxMzQ5Mw==&mid=100000033&idx=1&sn=8ab71afe95eba12030ed445de548fd4e&chksm=1fbacb9b28cd428d55bbf8a963e743b837b17f91a12401fa7dc93b8b08d28d0d49aecdfd5cf7#rd"
                }
            ]
        }
    ]
}"""
from dao.server_config import ServerConfigDao
accessToken = ServerConfigDao().getValue('kuxiao','access_token')
#myMenu.delete(accessToken)
myMenu.create(postJson, accessToken)
