#!/usr/bin/python
# -*- coding: utf-8 -*-


import webscreenshot
from webscreenshot import parser
import sys
reload(sys)
sys.setdefaultencoding('cp866')
import subprocess
print sys.argv

w = parser.parse_args()
print w

#options = {'proxy_type': None, 'workers': 2, 'log_level': 'DEBUG', 'http_username': None, 'input_file': None}
##options = {'proxy_type': None, 'workers': 2, 'http_username': None, 'input_file': 'olen.png','log_level': 'DEBUG', 'multiprotocol': False, 
    ##'output_directory': None, 'port': None, 'header': None, 'verbosity': 2, 
    ##'cookie': None, 'renderer': 'phantomjs', 'timeout': 30, 'proxy_auth': None, 
    ##'ssl': False, 'http_password': None, 'proxy': None}
url_list = ['https://ffpmif.com/marketing']
#webscreenshot.main(options, arguments)
options = dict()
options['input_file'] = 'gde.txt'
options['Ukraine'] = 'Kiev'
options['USA'] = 'Washington'

my_dict = dict(one=1, two=2, three=3)

options ={'workers': 2, 'http_username': None, 'input_file': 'gde.txt', 'multiprotocol': False, 'output_directory': None, 'port': None, 'header': None, 'proxy_type': None, 'verbosity': 1, 'cookie': None, 'renderer': 'phantomjs', 'timeout': 30, 'proxy_auth': None, 'ssl': False, 'http_password': None, 'proxy': None}
#for key, value in options.items():
    #print key, value
#w=options['workers'] = 1
#print options['workers']
webscreenshot.main()


#subprocess.Popen(["Python","python D:/webscreenshot/webscreenshot.py","name1","name2","name3"])

#from subprocess import Popen, PIPE
#Popen('python webscreenshot.py -v "https://ffpmif.com/marketing" -v', shell=True, stdout=PIPE).communicate()
#print(str(out, 'utf-8')) # или var = str(out, 'utf-8')

address = 'https://ffpmif.com/marketing'
port = 'gde.txt'

#{'workers': '1', 'http_username': None, 'input_file': 'gde.txt', 'multiprotocol': False, 'output_directory': None, 'port': None, 'header': None, 'proxy_type': None, 'verbosity': 1, 'cookie': None, 'renderer': 'phantomjs', 'timeout': 30, 'proxy_auth': None, 'ssl': False, 'http_password': None, 'proxy': None}

command = "python webscreenshot.py -i %s -w %d -v"%(port,1)
proc = subprocess.Popen(command, shell=True,universal_newlines=True).communicate()
print proc#[0].decode('utf-8').strip()

#string = "['-v', 'https://google.fr', 'arg3', 'arg4']" # строка с аргументами
#script = "webscreenshot.py" # путь к вашему скрипту

#os.system("{0} {1}".format(script, ' '.join(map(str, re.findall(r"\w+", string)))))
## вызовет команду /tmp/script.sh arg1 arg2 arg3 arg4 в шелле и перенаправит
## весь вывод в интерпретатор