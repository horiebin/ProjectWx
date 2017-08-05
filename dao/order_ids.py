from db_helper import DbHelper

from util.class_decorator import singleton

@singleton
class OrderIdsDao(object):
    def __init__(self):
        self.table = 'order_ids'
        self.db = DbHelper()

    def verifyByOrderID(self, orderid,shopid):
        val = {'orderId': orderid,'shopId':shopid}
        rows = self.db.select(self.table, where='order_id=$orderId and shop_id=$shopId', vars=val)
        if rows:
            return True
        else:
            return False