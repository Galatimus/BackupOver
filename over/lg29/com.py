#!/usr/bin/python
# -*- coding: utf-8 -*-



import logging
import time
import re
from grab import Grab
import random
from datetime import datetime,timedelta
import requests
from lxml import html
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
logging.basicConfig(level=logging.DEBUG)

page = requests.get('https://bcinform.moscow/arenda-ofisa/id16253/')
tree = html.fromstring(page.content)
print tree.xpath('//div[@class="extended-body"]')[0].text_content()
print tree.xpath('//div[@class="phone"]')[0].attrib['data-phone']
print tree.xpath('//meta[@name="keywords"]')[0].attrib['content'].split(', ')[1]
    
    
    
   