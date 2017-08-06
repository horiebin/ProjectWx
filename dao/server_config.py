from db_helper import DbHelper
from util.class_decorator import singleton
from util.memcache_util import Client
import config

@singleton
class ServerConfigDao(object):

    def __init__(self):
        self.table = 'server_config'
        self.db = DbHelper()
        self.pay_nameSpace = config.pay_namespace
        self.client = Client(config.prefix)


    def __getitem__(self, key):
        return self.getValue(self.pay_nameSpace,key)

    def setValue(self,namespace,key,value):
        self.client.set(namespace+'_'+key,value)
        val = {'name_space': namespace, 'k': key}
        self.db.update(self.table, where='name_space=$name_space and k=$k', vars=val,
                       v=value)

    def getValue(self,namespace,key):
        value = self.client.get(namespace+'_'+key)
        if not value:
            val = {'name_space': namespace, 'k': key}
            row = self.db.select(self.table, where='name_space=$name_space and k=$k', vars=val)[0]
            value = row.v
            self.client.set(namespace+'_'+key, value)
        return value

    def getNameSpaceByOriginalId(self, original_id):
        newKey = 'original_id_'+original_id
        value = self.client.get(newKey)
        if not value:
            val = {'v': original_id}
            row = self.db.select(self.table, where='k=\'original_id\' and v=$v', vars=val)[0]
            value = row.name_space
            self.client.set(newKey, value)
        return value

    def getAllNamespace(self):
        all = self.db.query('Select DISTINCT (name_space) from %s' % self.table)
        return [record['name_space'] for record in all]
