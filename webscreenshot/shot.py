#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import random
import logging
import subprocess
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logging.basicConfig(level=logging.DEBUG)

#g = Grab(timeout=20, connect_timeout=50)
#g.proxylist.load_file(path='ivan.txt',proxy_type='http')

#url = 'https://ffpmif.com/marketing'

#print sys.argv

#options = {'proxy_type': None, 'workers': 2, 'http_username': None, 'input_file': None, 'multiprotocol': False, 
           #'output_directory': None, 'port': None, 'header': None, 'verbosity': 2, 
           #'cookie': None, 'renderer': 'phantomjs', 'timeout': 30, 'proxy_auth': None, 
           #'ssl': False, 'http_password': None, 'proxy': None}
#webscreenshot.take_screenshot(url,{'workers': 1, 'workers': 2, 'http_username': None, 'input_file': None, 'multiprotocol': False, 
           #'output_directory': None, 'port': None, 'header': None, 'verbosity': 2, 
           #'cookie': None, 'renderer': 'phantomjs', 'timeout': 30, 'proxy_auth': None, 
           #'ssl': False, 'http_password': None, 'proxy': None})
           
#webscreenshot.take_screenshot(url, 'workers': 2)
#webscreenshot.main()

#options = {'proxy_type': None, 'workers': 2, 'log_level': 'DEBUG', 'http_username': None, 'input_file': None}
#url_and_options = url, options 

#webscreenshot.craft_cmd(url_and_options)

#options = {'proxy_type': None, 'workers': 2, 'log_level': 'DEBUG', 'http_username': None, 'input_file': None}

#webscreenshot.shell_exec(url, command, options=options)



l= open('gde.txt').read().splitlines()

#options = {'proxy_type': None, 'workers': 2, 'log_level': 'DEBUG', 'http_username': None, 'input_file': None}

#take_screenshot('https://ffpmif.com/marketing', options=options)

for p in range(len(l)):
    print '******',p+1,'/',len(l),'*******'
    proxy = random.choice(list(open('ivan.txt').read().splitlines())).split(':')[0]+':8080'
    print proxy
    address = l[p]
    command = "phantomjs --ignore-ssl-errors true --ssl-protocol any --load-images false --ssl-ciphers ALL --proxy-type http --proxy %s --proxy-auth %s fetch.js %s" % (proxy,'Ivan:tempuvefy',address)
    proc = subprocess.Popen(command, shell=True,stdout=subprocess.PIPE).communicate()
    print proc[0].decode('utf-8').strip()    
    #os.system('python webscreenshot.py -v '+l[p]+' -v'+' -P '+proxy+':8080'+' -A Ivan:tempuvefy')
    #os.system('python webscreenshot.py -v '+l[p]+' -v')
    time.sleep(0.2)
    