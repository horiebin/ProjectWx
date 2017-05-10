# -*- coding: utf-8 -*-
from basic import Basic
import urllib

class Media(object):
    def __init__(self):
        pass

    '''create temp media,
        type: image, vocie, video ,thumb;
        media: form-data中媒体文件标识，有filename、filelength、content-type等信息'''
    def create_temp(self,media_type,media, ccess_token):
        postUrl = "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=ACCESS_TOKEN&type=TYPE"
        postData = r"""{
                        type:"""+media_type+","+"""
                        media:"""+media+"""
        }"""
        if isinstance(postData, unicode):
            postData = postData.encode('utf-8')
        urlResp = urllib.urlopen(url=postUrl, data=postData)
        print urlResp.read()

    def download_temp(self, access_token, media_id):
        postUrl = "https://api.weixin.qq.com/cgi-bin/media/get?access_token=ACCESS_TOKEN&media_id=MEDIA_ID"
        urlResp = urllib.urlopen(url=postUrl)
        return urlResp.read()

    '''
     #get the permantent media list
     type:image,voice,video,news
     count: 0-20
     offset
    '''
    def get_media_list(self, access_token):
        postUrl = "https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token=%s" % accessToken
        postData = r"""
                    {
                        "type": "news",
                        "offset":0,
                        "count":3 
                    }
                   """
        if isinstance(postData, unicode):
            postData = postData.encode('utf-8')
        urlResp = urllib.urlopen(url=postUrl, data=postData)
        print urlResp.read()

if __name__ == '__main__':
    myMedia=Media()
    accessToken = Basic().get_access_token()

    myMedia.get_media_list( accessToken)
