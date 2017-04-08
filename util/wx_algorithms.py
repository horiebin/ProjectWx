import string
import random
import hashlib

def id_generator(size=16, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def js_signature(noncestr,jsapi_ticket,timestamp,url):
    s = "jsapi_ticket=%s&noncestr=%s&timestamp=%d&url=%s" %(jsapi_ticket,
                                                              noncestr,timestamp,url)
    h = hashlib.sha1(s)
    return h.hexdigest()
