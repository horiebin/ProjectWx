from db_helper import DbHelper

from util.class_decorator import singleton

@singleton
class LogShopMoneyDao(object):
    def __init__(self):
        self.table = 'log_change_money'
        self.db = DbHelper()

    def getMoneyByShopId(self,shopid):
        val = {'shopId': shopid}
        rows = self.db.select(self.table, where='shop_id=$shopId', vars=val,order='create_time desc',limit=1)
        return rows[0]['money']