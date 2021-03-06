import imp
import config
try:
    imp.find_module('pylibmc')
    import pylibmc as mc
except ImportError:
    import memcache as mc

class Client():
    def __init__(self, prefix):
        self.client = mc.Client(config.memcached_servers)
        self.prefix = prefix

    def set(self,key,value):
        key =  self.prefix + key
        return self.client.set(key,value)

    def get(self,key):
        key = self.prefix + key
        return self.client.get(key)
