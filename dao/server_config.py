from db_helper import DbHelper
from util.class_decorator import singleton
from util.memcache_util import Client
import config

@singleton
class ServerConfigDao(object):

    def __init__(self):
        self.table = 'server_config'
        self.db = DbHelper()
        self.nameSpace = 'wx'
        self.client = Client(config.prefix)


    def get_access_token(self):
        return self.getValue('access_token')

    def set_access_token(self,token):
        return self.setValue('access_token',token)

    def get_jsapi_ticket(self):
        return self.getValue('jsapi_ticket')

    def set_jsapi_ticket(self,jsTicket):
        self.setValue('jsapi_ticket',jsTicket)

    def getGlobalByKey(self,k):
        val = {'name_space':self.nameSpace,'k':k}
        row = self.db.select(self.table,where='name_space=$name_space and k=$k',vars=val)[0]
        return row.v

    def getAppId(self):
        return self.getValue['app_id']

    def getAppSecret(self):
        return self.getValue['app_secret']

    def __getitem__(self, key):
        return self.getValue(key)

    def setValue(self,key,value):
        self.client.set(key,value)
        val = {'name_space': self.nameSpace, 'k': key}
        self.db.update(self.table, where='name_space=$name_space and k=$k', vars=val,
                       v=value)

    def getValue(self,key):
        access_token = self.client.get(key)
        if not access_token:
            access_token = self.getGlobalByKey(key)
            self.client.set(key, access_token)
        return access_token