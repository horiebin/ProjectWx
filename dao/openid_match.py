from db_helper import DbHelper

from util.class_decorator import singleton

@singleton
class OpenidMatch(object):
    def __init__(self):
        self.table = 'openid_match'
        self.db = DbHelper()

    def insertSourceUser(self,openid,namespace):
        try:
            self.db.insert(self.table,source_openid=openid,source_namespace=namespace)
        except :
            return False
        return True

    def insertPayUser(self,openid,source_openid):
        val = { 'source_openid': source_openid}
        self.db.update(self.table, where='source_openid=$source_openid', vars=val,
                       pay_openid=openid)