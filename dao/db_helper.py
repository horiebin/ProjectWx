from util.class_decorator import singleton
import web
from config import config

@singleton
class DbHelper(object):

    def __init__(self):
        print('init database')
        self.db = web.database(host=config['host'],port=config['port'], dbn=config['dbn']
                               , user=config['username'], pw=config['password'], db=config['dbname'])

    def select(self, *args, **kw):
        return self.db.select(*args, **kw)

    def insert(self,*args,  **kw):
        return self.db.insert(*args, **kw)

    def update(self,*args,  **kw):
        return self.db.update(*args, **kw)

