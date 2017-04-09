import socket
from util.class_decorator import singleton

@singleton
class Config(object):
    config_husonchen = {
        'server': 'localhost:8080',
        'dbn': 'mysql',
        'username': 'projectwx_user',
        'password': 'pw2017-03-22',
        'dbname': 'projectwx',
        'host': 'localhost',
        'port': 3306,
        'appId': 'wx87ea3850b33bdfcb',
    }

    config_server = {
        'server': 'sickworm.com',
        'dbn': 'mysql',
        'username': 'xiaob',
        'password': 'skdfjkasdf',
        'dbname': 'xiaob',
        'host': 'localhost',
        'port': 3306,
        'appId': 'wx87ea3850b33bdfcb',
    }

    config_develop = {
        'server': 'sickworm.com',
        'dbn': 'mysql',
        'username': 'projectwx_user',
        'password': 'pw2017-03-22',
        'dbname': 'projectwx',
        'host': 'localhost',
        'port': 3306,
        'appId': 'wx87ea3850b33bdfcb',
    }

    def __init__(self):
        myname = socket.getfqdn(socket.gethostname())
        if myname == 'iZ94mm9cb9hZ':
            print('server is running on %s ... configurating..' % myname)
            self.config = self.config_server
        else:
            print('server is running on develop mod...configurating..')
            self.config = self.config_develop

    def __getitem__(self, key):
        return self.config[key]