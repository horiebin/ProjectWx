import requests
import config
import json

class NsqProducer():
    def __init__(self,topic):
        self.topic = topic
        self.murl = u'http://' + config.nsqd+'/mpub?topic=' + topic
        self.url = u'http://' + config.nsqd+'/pub?topic=' + topic


    def produce(self,message):
        m = json.dumps(message)
        requests.post(self.url, data=m)

    def produceList(self,messages):
        payload = [json.dumps(m) for m in messages]
        p = '\n'.join(payload)
        requests.post(self.murl,data=p)