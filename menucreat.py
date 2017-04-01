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
            "url":  "http://husonchen.com/refund"
        },
        {
            "name": "贴膜教程",
            "sub_button":
            [
                {
                    "type": "view_limited",
                    "name": "手机前膜",
                    "media_id": "gBJQzVNDqjRfDVaFjCoNpNoltBLj2IiSVqGxvbgiMhc"
                },
                {
                    "type": "view_limited",
                    "name": "手机后膜",
                    "media_id": "gBJQzVNDqjRfDVaFjCoNpNA9aL2swEwR1JUPXej8bog"
                },
                {
                    "type": "view_limited",
                    "name": "去白边",
                    "media_id": "gBJQzVNDqjRfDVaFjCoNpOx2fX9Wc7pr18_EldCaFXE"
                }
            ]
        },
        {
            "type": "view",
            "name": "优选商品推荐",
            "url": "http://husonchen.com/adforgoods"
        }
      ]
}"""

accessToken = Basic().get_access_token()
#myMenu.delete(accessToken)
myMenu.create(postJson, accessToken)
