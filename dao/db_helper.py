
from util.class_decorator import singleton
import web
from config import Config

@singleton
class DbHelper(object):

    def __init__(self):
        config = Config()
        print('init database %s' % config['dbname'])
        self.db = web.database(host=config['host'],port=config['port'], dbn=config['dbn']
                               , user=config['username'], pw=config['password'], db=config['dbname'])

    def select(self, *args, **kw):
        return self.db.select(*args, **kw)

    def insert(self,*args,  **kw):
        return self.db.insert(*args, **kw)

    def update(self,*args,  **kw):
        return self.db.update(*args, **kw)

    def query(self,*args,  **kw):
        return self.db.query(*args, **kw)