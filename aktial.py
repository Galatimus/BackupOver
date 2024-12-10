#!/usr/bin/python
# -*- coding: utf-8 -*-
import xlrd
import time
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
rb = xlrd.open_workbook(u'C:/Users/Oleg/Desktop/Результат.xlsx',on_demand=True)
sheet = rb.sheet_by_index(0)
workbook = xlsxwriter.Workbook(u'C:/Users/Oleg/Desktop/Актуальность_КН.xlsx')
ws = workbook.add_worksheet()   
ws.write(0,0, u"КодПредложения")
ws.write(0,1, u"Источник")
ws.write(0,2, u"Ссылка")
ws.write(0,3, u"Актуальность")
row = 1
i = 0
l= open('actual.txt').read().splitlines()
for ak in range(1,sheet.nrows):
       #time.sleep(0.0001)
       links = sheet.cell_value(ak,2)
       try:
              cod = '%d'%(sheet.cell_value(ak,0))
       except TypeError:
              cod = '%s'%(sheet.cell_value(ak,0))
       ist = sheet.cell_value(ak,1).lower()
       akt = sheet.cell_value(ak,3)
       i=i+1
       page = l[i]
       if akt == '':
              akt = page
       ws.write_string(row, 0, cod)
       ws.write(row, 1, ist)
       ws.write_string(row, 2, links)
       ws.write(row, 3, akt) 
       row+= 1
       print 'Ready - '+str(row)+'/'+str(sheet.nrows)+'/'+str(cod)
time.sleep(1)
print('Wait ...')
workbook.close()
print('Done!') 
