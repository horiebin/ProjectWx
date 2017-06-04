from db_helper import DbHelper

from util.class_decorator import singleton
from util.memcache_util import Client
import config

@singleton
class AutoReplyDao(object):
    def __init__(self):
        self.table = 'auto_reply'
        self.db = DbHelper()
        self.client = Client(config.prefix)

    def getAllReplys(self):
        rows = self.client.get('auto_reply')
        if not rows:
            rows = self.db.select(self.table, where='enable_flag=1',order='id asc')
            self.client.set('auto_reply',list(rows))
        return rows