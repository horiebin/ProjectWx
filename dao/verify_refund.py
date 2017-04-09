from db_helper import DbHelper

class VerifyRefundDao(object):
    def __init__(self):
        self.table = 'verify_refund'
        self.db = DbHelper()

    def selectByOpenId(self,openId):
        # return 30 rows
        val = {'openId':openId}
        rows = self.db.select(self.table,where='open_id=$openId',vars=val,order='update_time desc',limit=30)
        return rows