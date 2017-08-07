from db_helper import DbHelper

from util.class_decorator import singleton

@singleton
class OrderIdsDao(object):
    def __init__(self):
        self.table = 'order_ids'
        self.db = DbHelper()

    def verifyByOrderID(self, orderid):
        val = {'orderId': orderid}
        rows = self.db.select(self.table, where='order_id=$orderId', vars=val)
        if rows:
            return rows[0]
        else:
            return False