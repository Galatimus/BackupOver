#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import glob
import csv
from xlsxwriter.workbook import Workbook
import sys
import logging
import time
reload(sys)
sys.setdefaultencoding('utf-8')

logging.basicConfig(level=logging.DEBUG)


for csvfile in glob.glob(os.path.join('.', '*.csv')):
         workbook = Workbook(csvfile[:-4] + '.xlsx')
         worksheet = workbook.add_worksheet()
         with open(csvfile, 'r') as f:
                  reader = csv.reader(f)
                  for r, row in enumerate(reader):
                           for c, col in enumerate(row):
                                    worksheet.write_string(r, c, col)
         workbook.close()






 

