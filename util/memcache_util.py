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
	try:
	    print 'memcache set:'+key+':'+value
	except:
	    print 'memcache set:'+key
        return self.client.set(key,value)

    def get(self,key):
        key = self.prefix + key
        value = self.client.get(key)
	try:
	    print 'memcache get:'+key+':'+value
	except:
	    print 'memcache get:'+key
	    import traceback
 	    print traceback.format_exc()
	return value
