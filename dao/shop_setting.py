from db_helper import DbHelper

from util.class_decorator import singleton

@singleton
class ShopSettingDao(object):
    def __init__(self):
        self.table = 'shop_setting'
        self.db = DbHelper()

    def getSetting(self, shopid):
        val = {'shopId': shopid}
        rows = self.db.select(self.table, where='shop_id=$shopId', vars=val)
        return rows[0]