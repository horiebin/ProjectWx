from db_helper import DbHelper

class ServerConfigDao(object):
    def __init__(self):
        self.table = 'server_config'
        self.db = DbHelper()

    def get_access_token(self):
        val = {'name_space': 'global', 'k': 'access_token'}
        row = self.db.select(self.table,where='name_space=$name_space and k=$k',vars=val)[0]
        return row.v

    def set_access_token(self,token):
        val = {'name_space': 'global', 'k': 'access_token'}
        self.db.update(self.table,where='name_space=$name_space and k=$k',vars=val,
                       v=token)

    def get_jsapi_ticket(self):
        val = {'name_space': 'global', 'k': 'jsapi_ticket'}
        row = self.db.select(self.table, where='name_space=$name_space and k=$k', vars=val)[0]
        return row.v

    def set_jsapi_ticket(self,jsTicket):
        val = {'name_space': 'global', 'k': 'jsapi_ticket'}
        self.db.update(self.table,where='name_space=$name_space and k=$k',vars=val,
                       v=jsTicket)

