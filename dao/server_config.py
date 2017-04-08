from db_helper import DbHelper

class ServerConfig(object):
    def __init__(self):
        self.table = 'server_config'
        self.db = DbHelper()
        self.val = {'name_space':'global','k':'access_token'}
    def get_access_token(self):

        row = self.db.select(self.table,where='name_space=$name_space and k=$k',vars=self.val)[0]
        return row.access_token

    def set_access_token(self,token):
        self.db.update(self.table,where='name_space=$name_space and k=$k',vars=self.val,
                       v=token)

