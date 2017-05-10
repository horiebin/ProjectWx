 # -*- coding: utf-8 -*-

from menu import Menu
from basic import Basic

myMenu = Menu()
postJson ="""
{
    "button":
    [
        {
            "type": "view",
            "name": "好评返现",
            "url":  "http://we.xwpay.sickworm.com/refund/oauth?shopid=23333"
        },
        {
            "name": "贴膜教程",
            "sub_button":
            [
                {
                    "type": "view_limited",
                    "name": "手机前膜",
                    "media_id": "DcD0PZMr1i__9B_jmvqWleB8Y52i2Bcaq6UKbo00qq0"
                },
                {
                    "type": "view_limited",
                    "name": "手机后膜",
                    "media_id": "DcD0PZMr1i__9B_jmvqWlYfsumCNM6lBR7rBiJHsMCg"
                },
                {
                    "type": "view_limited",
                    "name": "去白边",
                    "media_id": "DcD0PZMr1i__9B_jmvqWlaOnwcbSlpsO_1PgyF2dyA0"
                }
            ]
        }
      ]
}"""

accessToken = Basic().get_access_token()
#myMenu.delete(accessToken)
myMenu.create(postJson, accessToken)
