from db_helper import DbHelper

class UserUploadDao(object):
    def __init__(self):
        self.table = 'user_upload'
        self.db = DbHelper()

    def insert(self,openId,orderId,imageId1='',imageId2='',imageId3=''):
        self.db.insert(self.table,open_id=openId,order_id=orderId,
                       image1_id=imageId1,image2_id=imageId2,image3_id=imageId3)
        return True
