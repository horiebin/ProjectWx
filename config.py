import socket
from util.class_decorator import singleton
# from dao.server_config import ServerConfigDao

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
        'appId': '',
        'appSecret': '',
    }

    config_server = {
        'server': 'we.xwpay.sickworm.com',
        'dbn': 'mysql',
        'username': 'xiaob',
        'password': 'skdfjkasdf',
        'dbname': 'xiaob',
        'host': 'localhost',
        'port': 3306,
        'appId': '',
        'appSecret': '',
    }

    config_develop = {
        'server': 'we.xwpay.sickworm.com',
        'dbn': 'mysql',
        'username': 'xiaob',
        'password': 'skdfjkasdf',
        'dbname': 'xiaob',
        'host': 'localhost',
        'port': 3307,
        'appId': '',
        'appSecret': '',
    }

    def __init__(self):
        myname = socket.getfqdn(socket.gethostname())
        if myname == 'iZ94mm9cb9hZ':
            print('server is running on %s ... configurating..' % myname)
            self.config = self.config_server
        else:
            print('server is running on develop mod...configurating..')
            self.config = self.config_develop

        # self.config['appId'] = ServerConfigDao().getGlobalByKey('app_id')
        # self.config['appSecret'] = ServerConfigDao().getGlobalByKey('app_secret')

    def __getitem__(self, key):
        return self.config[key]
