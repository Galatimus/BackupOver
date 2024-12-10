#!/usr/bin/env python
import sys
import six
import time
from six.moves.urllib import request
import json
print sys.version_info[0]
lin = []
for p in range(650):
    time.sleep(60)    
    opener = request.build_opener(request.ProxyHandler({'http': 'http://lum-customer-landly-zone-zone1:e7qhy6dhu0fs@zproxy.lum-superproxy.io:22225'}))
    proxy = json.load(opener.open('http://lumtest.com/myip.json'))
    host = proxy['ip']
    port = '22225'
    my_proxy = 'http://'+host+':'+port
    print my_proxy
    lin .append(my_proxy)
links = open('lumtest.txt', 'a')
for item in lin:
    links.write("%s\n" % item)
links.close()