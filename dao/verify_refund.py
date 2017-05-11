from db_helper import DbHelper

from util.class_decorator import singleton

@singleton
class VerifyRefundDao(object):
    def __init__(self):
        self.table = 'verify_refund'
        self.db = DbHelper()

    def selectByOpenId(self,shopid,openId):
        # return 30 rows
        val = {'shopId':shopid,'openId':openId}
        rows = self.db.select(self.table,where='shop_id=$shopId and open_id=$openId',vars=val,order='update_time desc',limit=30)
        return rows

    def insertVerifyRefund(self,shopId,openId,orderId,money):
        self.db.insert(self.table,shop_id=shopId,open_id=openId,order_id=orderId,money=money)
        return True


    def selectByPage(self,page_size):
        rows = self.db.select(self.table,where='refund_flag=0 and del_flag=0',order='id asc',limit=page_size)
        return rows

    def setRefundFlag(self,id):
        val = {'id':id}
        self.db.update(self.table,where='id=$id',vars=val,refund_flag=1)