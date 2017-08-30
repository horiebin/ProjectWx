from db_helper import DbHelper
from util.memcache_util import Client
import config
from util.class_decorator import singleton

@singleton
class MpInfoDao(object):
    def __init__(self):
        self.table = 'mp_info'
        self.db = DbHelper()
        self.client = Client(config.prefix+'_mp_info_')

    def getSettingById(self, id):
        key = 'id_' + id
        value = self.client.get(key)
        if not value:
            val = {'id': id}
            rows = self.db.select(self.table, where='id=$id', vars=val)
            value = rows[0]
            self.client.set(key,value)
        return value

    def getSettingByAppid(self, app_id):
        key = 'appid_' + app_id
        value = self.client.get(key)
        if not value:
            val = {'authorizer_appid': app_id}
            rows = self.db.select(self.table, where='authorizer_appid=$authorizer_appid', vars=val)
            value = rows[0]
            self.client.set(key, value)
        return value

