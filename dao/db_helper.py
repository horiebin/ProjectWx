from util.class_decorator import singleton
import web

@singleton
class DbHelper(object):
    dbn = 'mysql'
    username = 'projectwx_user'
    password = 'pw2017-03-22'
    dbname = 'projectwx'
    host = 'localhost'
    port = 3306
    def __init__(self):
        print('init database')
        self.db = web.database(host=self.host,port=self.port, dbn=self.dbn, user=self.username, pw=self.password, db=self.dbname)

    def select(self, *args, **kw):
        return self.db.select(*args, **kw)

    def insert(self,*args,  **kw):
        return self.db.insert(*args, **kw)

    def update(self,*args,  **kw):
        return self.db.update(*args, **kw)

