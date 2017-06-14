from db_helper import DbHelper

from util.class_decorator import singleton

@singleton
class UserBelongDao(object):
    def __init__(self):
        self.table = 'user_belong'
        self.db = DbHelper()

    def insertOnUpdate(self,open_id,shop_id):
        try:
            self.db.insert(self.table,open_id=open_id,shop_id=shop_id,create_time=None, update_time=None)
        except :
            vals = {'openId':open_id,'shopId':shop_id}
            self.db.update(self.table,where="open_id=$openId and shop_id!=$shopId",vars=vals,shop_id=shop_id)
        return True

    def getShopIdByOpenId(self,open_id):
        val = {'openId': open_id}
        rows = self.db.select(self.table, where='open_id=$openId', vars=val)
        if rows:
            return rows[0]['shop_id']
        return False