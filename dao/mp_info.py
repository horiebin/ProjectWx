from db_helper import DbHelper

from util.class_decorator import singleton

@singleton
class MpInfoDao(object):
    def __init__(self):
        self.table = 'mp_info'
        self.db = DbHelper()

    def getSettingById(self, id):
        val = {'id': id}
        rows = self.db.select(self.table, where='id=$id', vars=val)
        return rows[0]

    def getSettingByAppid(self, app_id):
        val = {'authorizer_appid': app_id}
        rows = self.db.select(self.table, where='authorizer_appid=$authorizer_appid', vars=val)
        return rows[0]