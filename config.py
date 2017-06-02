import socket
from util.class_decorator import singleton
# from dao.server_config import ServerConfigDao

import logging

file = "logs/webpy.log"
logformat = "[%(asctime)s] %(filename)s:%(lineno)d(%(funcName)s): [%(levelname)s] %(message)s"
datefmt = "%Y-%m-%d %H:%M:%S"
loglevel = logging.INFO
interval = "d"
backups = 7

@singleton
class Config(object):

    config_server = {
        'dbn': 'mysql',
        'username': 'xiaob',
        'password': 'skdfjkasdf',
        'dbname': 'xiaob',
        'host': 'localhost',
        'port': 3306,
    }

    config_develop = {
        'dbn': 'mysql',
        'username': 'xiaob',
        'password': 'skdfjkasdf',
        'dbname': 'xiaob',
        'host': 'localhost',
        'port': 3306,
    }

    def __init__(self):
        myname = socket.getfqdn(socket.gethostname())
        print('server is running on %s ... configurating..' % myname)
        self.config = self.config_server

    def __getitem__(self, key):
        return self.config[key]
