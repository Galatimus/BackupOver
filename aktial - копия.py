#!/usr/bin/python
# -*- coding: utf-8 -*-


from threading import Thread





import xlrd
import time
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


rb = xlrd.open_workbook(u'C:/Users/Oleg/Desktop/Книга-2.xlsx',on_demand=True)
sheet = rb.sheet_by_index(0)
rb1 = xlrd.open_workbook(u'C:/Users/Oleg/Desktop/Actcom2.xlsx',on_demand=True)
sheet1 = rb1.sheet_by_index(0)



workbook = xlsxwriter.Workbook(u'C:/Users/Oleg/Desktop/АктКН.xlsx')
ws = workbook.add_worksheet()   
ws.write(0,0, u"КодПредложения")
ws.write(0,1, u"Источник")
ws.write(0,2, u"Ссылка")
ws.write(0,3, u"Актуальность")
row= 1 


def loopA():
       for ak in range(1,sheet.nrows):
              time.sleep(0.0001)
              links = sheet.cell_value(ak,2)
              cod = sheet.cell_value(ak,0)       
              ist = sheet.cell_value(ak,1)
              akt = sheet.cell_value(ak,3)
              print links

def loopB():
       for ak1 in range(1,sheet1.nrows):
              time.sleep(0.0001)
              links1 = sheet1.cell_value(ak1,2)
              cod1 = sheet1.cell_value(ak1,0)       
              ist1 = sheet1.cell_value(ak1,1)
              akt1 = sheet1.cell_value(ak1,3)
              print links1

threadA = Thread(target = loopA)
threadB = Thread(target = loobB)
threadA.run()
threadB.run()
# Do work indepedent of loopA and loopB 
threadA.join()
threadB.join()       
       
#for ak in range(1,sheet.nrows):
       ##time.sleep(0.0001)
       #links = sheet.cell_value(ak,2)
       #cod = sheet.cell_value(ak,0)       
       #ist = sheet.cell_value(ak,1)
       #akt = sheet.cell_value(ak,3)

#for ak1 in range(1,sheet1.nrows):
       ##time.sleep(0.0001)
       #links1 = sheet1.cell_value(ak1,2)
       #cod1 = sheet1.cell_value(ak1,0)       
       #ist1 = sheet1.cell_value(ak1,1)
       #akt1 = sheet1.cell_value(ak1,3)