import imp
import config
try:
    imp.find_module('pylibmc')
    import pylibmc as mc
except ImportError:
    import memcache as mc
from web.utils import ThreadedDict

class Client():
    def __init__(self, prefix):
        self.d = ThreadedDict()
        self.d.client = mc.Client(config.memcached_servers)
        self.prefix = prefix

    def set(self,key,value):
        key =  self.prefix + key
	try:
	    print 'memcache set:'+key+':'+value
	except:
	    print 'memcache set:'+key
        return self.d.client.set(key,value)

    def get(self,key):
        key = self.prefix + key
        value = self.d.client.get(key)
	try:
	    print 'memcache get:'+key+':'+value
	except:
	    print 'memcache get:'+key
	    import traceback
 	    print traceback.format_exc()
	return value
