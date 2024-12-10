#!/usr/bin/python
# -*- coding: utf-8 -*-

import xlrd
import csv
import sys
import logging
import time
reload(sys)
sys.setdefaultencoding('utf-8')

logging.basicConfig(level=logging.DEBUG)


wb = xlrd.open_workbook('bornprettystore2.xlsx',on_demand=True)
sh = wb.sheet_by_index(0)
your_csv_file = open('bornn.csv', 'w')
wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)
for rownum in range(sh.nrows):
         wr.writerow(sh.row_values(rownum))

your_csv_file.close()






 

