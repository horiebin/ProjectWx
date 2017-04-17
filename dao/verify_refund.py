from db_helper import DbHelper

class VerifyRefundDao(object):
    def __init__(self):
        self.table = 'verify_refund'
        self.db = DbHelper()

    def selectByOpenId(self,shopid,openId):
        # return 30 rows
        val = {'shopId':shopid,'openId':openId}
        rows = self.db.select(self.table,where='shop_id=$shopId and open_id=$openId',vars=val,order='update_time desc',limit=30)
        return rows