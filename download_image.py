# this file is to download wechat image from wechat server
import urllib
from dao.server_config import ServerConfigDao
from dao.user_upload import UserUploadDao
from threading import Timer
import os
import traceback

targetDir = r'/home/huson/admin.51dingxiao.com/static/wx_temp'

def downloadByAccessTokenAndMediaId(accessToken,mediaId):
    url = r'http://file.api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s' % (accessToken, mediaId)
    urllib.urlretrieve(url, "%s/%s.jpg" % (targetDir,mediaId))

def start_download():
    try:
        access_token = ServerConfigDao().get_access_token()
        file = open('current.id','r+')
        # once 100 images
        line = file.readline()
        if line != '':
            start = int(line)
        else :
            start = 0
        # file.close()
        # file = open('current.id','w+')
        print('last end at id=%d'%start)
        while True:
            rows = UserUploadDao().selectByPage(start+1,100)
            for row in rows:
                media1Id = row.image1_id
                if media1Id != '':
                    downloadByAccessTokenAndMediaId(access_token,media1Id)
                media2Id = row.image2_id
                if media2Id != '':
                    downloadByAccessTokenAndMediaId(access_token, media2Id)
                media3Id = row.image3_id
                if media3Id != '':
                    downloadByAccessTokenAndMediaId(access_token, media3Id)
                file.seek(0,0)
                file.write(str(row.id))
                file.flush()
                os.fsync(file)
            if len(rows) < 100:
                break
            else:
                start = row.id
        file.close()
    except:
        traceback.print_exc()

    #restart self every 30 seconds
    Timer(1 * 1, start_download, ()).start()

if __name__ == '__main__':
    start_download()
