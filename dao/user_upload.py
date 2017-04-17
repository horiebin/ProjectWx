from db_helper import DbHelper

class UserUploadDao(object):
    def __init__(self):
        self.table = 'user_upload'
        self.db = DbHelper()

    def insert(self,shopid,openId,orderId,imageId1='',imageId2='',imageId3=''):
        self.db.insert(self.table,shop_id=shopid,open_id=openId,order_id=orderId,
                       image1_id=imageId1,image2_id=imageId2,image3_id=imageId3,
                       create_time=None,update_time=None)
        return True

    def selectByOpenId(self,shopid,openId):
        val = {'shopId':shopid,'openId':openId}
        rows = self.db.select(self.table,where='shop_id=$shopId and open_id=$openId and del_flag=0 and verify_flag=0',
                              vars=val,order='create_time desc',limit=10)
        return rows