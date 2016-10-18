import httplib
import re
from AbstractDevice import AbstractDevice

class CubisDevice(AbstractDevice):
    
    def __init__(self, ip):
        self.ip = ip
        self.methods = []
        
    def getAllMethods(self):
        methods = dir(self)
        for m in methods:
            if m != '__doc__' and m!= '__init__' and m != '__module__' and m != 'getAllMethods' and m != 'ip' and m != 'methods':
                self.methods.append(m)
                
    def rightWindshieldKey(self):
        conn = httplib.HTTPConnection(self.ip)
        conn.request("PUT", "/rest1_0/PUT/appl/cmd/WINDSH/RGT_KEY")
        conn.close()
        
    def putText(self, text):
        conn = httplib.HTTPConnection(self.ip)
        conn.request("PUT", "/rest1_0/PUT/appl/ui/WORK/1/TEXT/1?text="+text)
        conn.close()
        
    def clearScreen(self):
        conn = httplib.HTTPConnection(self.ip)
        conn.request("PUT", "/rest1_0/DELETE/appl/ui/WORK/1")
        conn.close()     
        
    def doTare(self):   
        conn = httplib.HTTPConnection(self.ip)
        conn.request("PUT", "/rest1_0/PUT/appl/cmd/WEIGH/DO_ZEROTARE")
        conn.close()          
        
    def getWeight(self):
        conn = httplib.HTTPConnection(self.ip)
        conn.request("GET", "/rest1_0/GET/appl/par/WEIGH/WGT_NET")
        result = conn.getresponse()
        response = result.read()
        value = re.search('value="(.*)" unit', response)
        print value.group(1)
        conn.close