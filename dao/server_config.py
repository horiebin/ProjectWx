from db_helper import DbHelper
from util.class_decorator import singleton
from config import Config

@singleton
class ServerConfigDao(object):

    def __init__(self):
        self.table = 'server_config'
        self.db = DbHelper()
        self.nameSpace = Config()['server']
        self.config = {}
        self.loadServerConfig()


    def loadServerConfig(self):
        # load config into memery
        val = {'name_space':self.nameSpace}
        rows = self.db.select(self.table,where='name_space=$name_space',vars=val)
        for row in rows:
            self.config[row.k] = row.v
        print("finished load server configs")

    def get_access_token(self):
        return self.config['access_token']

    def set_access_token(self,token):
        self.config['access_token'] = token
        val = {'name_space': self.nameSpace, 'k': 'access_token'}
        self.db.update(self.table,where='name_space=$name_space and k=$k',vars=val,
                       v=token)

    def get_jsapi_ticket(self):
        return self.config['jsapi_ticket']

    def set_jsapi_ticket(self,jsTicket):
        self.config['jsapi_ticket'] = jsTicket
        val = {'name_space': self.nameSpace, 'k': 'jsapi_ticket'}
        self.db.update(self.table,where='name_space=$name_space and k=$k',vars=val,
                       v=jsTicket)

    def getGlobalByKey(self,k):
        val = {'name_space':self.nameSpace,'k':k}
        row = self.db.select(self.table,where='name_space=$name_space and k=$k',vars=val)[0]
        return row.v

    def getAppId(self):
        return self.config['app_id']

    def getAppSecret(self):
        return self.config['app_secret']