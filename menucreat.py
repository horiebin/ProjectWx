 # -*- coding: utf-8 -*-

from menu import Menu
from basic import Basic

myMenu = Menu()
postJson ="""
{
    "button":
    [
        {
            "name": "返现售后",
            "sub_button":
            [
                {
                    "type": "view",
                    "name": "五星好评返现",
                    "url": "http://we.xwpay.sickworm.com/refund/oauth?shopid=10000"
                },
                {
                    "type":"view_limited",
                    "name": "关于售后",
                    "media_id":"DcD0PZMr1i__9B_jmvqWlSJOQCiIl8W-Cca-Zr_zeWM"
                }

            ]
        },
        {
            "name": "产品介绍",
            "sub_button":
            [
                {
                    "type": "view_limited",
                    "name": "非全屏钢化膜",
                    "media_id":"DcD0PZMr1i__9B_jmvqWldj2HtvukYuGC6Ne5kpvwQM"
                },
                {
                    "type": "view_limited",
                    "name": "丝印全屏膜",
                    "media_id": "DcD0PZMr1i__9B_jmvqWlaEIAcOkWTbDI46voB0PqA0"
                },
                {
                    "type": "view_limited",
                    "name": "抗蓝光钢化膜",
                    "media_id":"DcD0PZMr1i__9B_jmvqWlbpWaRHog897LE_BajZR8uE"
                },
                {
                    "type": "view_limited",
                    "name": "软边钢化膜",
                    "media_id":"DcD0PZMr1i__9B_jmvqWlaPG2UumvBvDTZOUG815WkU"
                },
                {
                    "type": "view_limited",
                    "name": "碳纤维后膜",
                    "media_id":"DcD0PZMr1i__9B_jmvqWlXNmAjqAh0vt66AyUvJUZvA"
                }
            ]
        },
        {
            "name": "贴膜教学",
            "sub_button":
            [
                {
                    "type": "view_limited",
                    "name": "贴膜教学",
                    "media_id":"DcD0PZMr1i__9B_jmvqWlZU2vp4HG42zc7OC8ufaq9k"
                },
                {
                    "type": "view_limited",
                    "name": "灰尘去除方法",
                    "media_id":"DcD0PZMr1i__9B_jmvqWlb7SwEitulOFNr6t3SNZGDE"
                },
                {
                    "type": "view_limited",
                    "name": "白边修复方法",
                    "media_id":"DcD0PZMr1i__9B_jmvqWlTQuv4isig1UPAl2190E3ds"
                },
                {
                    "type": "view_limited",
                    "name": "气泡去除方法",
                    "media_id":"DcD0PZMr1i__9B_jmvqWlcl-sP0YFYCFcrCNlbdl0gM"
                },
                {
                    "type": "view_limited",
                    "name": "贴后膜方法",
                    "media_id":"DcD0PZMr1i__9B_jmvqWlauzwxyu8bP-qXG97XGFBGM"
                }
            ]
        }
      ],
  "matchrule":{
  "tag_id":"101"
  }

}"""

accessToken = Basic().get_access_token()
#myMenu.delete(accessToken)
myMenu.createCondition(postJson, accessToken)
