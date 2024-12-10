#!/usr/bin/env python
# -*- coding: utf-8 -*-



import os
import time
from os import listdir
import csv
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



l= open('city.txt').read().splitlines()

try:
        for p in range(184,len(l)):
                print '**',p,'/',len(l),'**'
                find = l[p].split(',')[0]
                workbook = xlsxwriter.Workbook('ready/'+str(find)+'_new.xlsx')    
                ws = workbook.add_worksheet()
                ws.write(0, 0, "NUMBER")
                ws.write(0, 1, "STREET")
                ws.write(0, 2, "CITY")
                ws.write(0, 3, "POSTCODE")
                result= 1                
                for root, dirs, files in os.walk("/home/oleg/pars/city"):
                        for file in files:
                                if file.endswith(".csv"):
                                        with open(os.path.join(root, file)) as csvfile:
                                                reader = csv.DictReader(csvfile)
                                                print 'Name IS >>> '+ str(file)
                                                #if find.lower().replace(' ','_')+'.csv' == str(file).replace('city_of_',''):
                                                        #for row in reader:
                                                                #time.sleep(0.001)
                                                                #print row['NUMBER'],row['STREET'].title(),find,row['POSTCODE']
                                                                #ws.write_string(result, 0, row['NUMBER'])
                                                                #ws.write_string(result, 1, row['STREET'].title())
                                                                #ws.write_string(result, 2, find)
                                                                #ws.write_string(result, 3, row['POSTCODE'])
                                                                #result+=1
                                        #else:
                                                for row in reader:
                                                        if find == row['CITY'].title():
                                                                print row['NUMBER'], row['STREET'].title(),row['CITY'].title(),row['POSTCODE']
                                                                ws.write_string(result, 0, row['NUMBER'])
                                                                ws.write_string(result, 1, row['STREET'].title())
                                                                ws.write_string(result, 2, find)
                                                                ws.write_string(result, 3, row['POSTCODE'])
                                                                result+=1                                                        
                                                        
                        print '***',result,'***',str(find),'***',str(p),'/',len(l),'**'
                print('Save it...')
                workbook.close()
                time.sleep(1)
                print('Done')                
                print '**',p,'/',len(l),'**'
                time.sleep(1)
except KeyboardInterrupt:
        pass
time.sleep(1)
print('Done ALL')



