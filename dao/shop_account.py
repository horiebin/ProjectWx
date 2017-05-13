from db_helper import DbHelper

from util.class_decorator import singleton

@singleton
class ShopAccountDao(object):
    def __init__(self):
        self.table = 'shop_account'
        self.db = DbHelper()

    def reduceMoney(self, shopid,money):
        val = {'money': money,'shopid':shopid}
        effectRows = self.db.db.query('update shop_account set balance=balance-$money where shop_id=$shopid and balance>=$money', vars= val)
        return effectRows

    def addbackMoney(self,shopid,money):
        val = {'money': money, 'shopid': shopid}
        effectRows = self.db.db.query(
            'update shop_account set balance=balance+$money where shop_id=$shopid', vars=val)
        return effectRows