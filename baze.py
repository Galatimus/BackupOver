# -*- coding: utf-8 -*-
#!usr/bin/env python


import xlrd
import MySQLdb
import logging

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

# Open the workbook and define the worksheet
book = xlrd.open_workbook("dom.xlsx")
#sheet = book.sheet_by_name("source")

sheet = book.sheet_by_index(0)

# Establish a MySQL connection
database = MySQLdb.connect (host="109.68.190.240", user = "oleg", passwd = "walter2005", db = "rway",port = 33306,use_unicode=True,charset='utf8')

# Get the cursor, which is used to traverse the database, line by line
cursor = database.cursor()

print cursor

# Create the INSERT INTO sql query
query = """INSERT INTO com (SUBJECT,MUN_WARD,CITY,VGT,STREET,HOUSE,LANDMARK,SEGMENT,OBJ_TYPE,OBJ_USE,KLASS,PRICE,PRICE_CHANGE,PRICE_CONDITION,AREA,FLOR,FLOOR_TOTAL,YEAR_BUILT,DETAILS,SOURCE,URL_SOURCE,PHONE,SELLER,COMPANY,FULL_ADDRESS,OTHER_ADDRESS,
METRO,METRO_DISTANCE,OPERACIA,DATE_CREATE,DATE_UPDATE,DATE_PARS,CAD_NUMB,TITLE,LATITUDE_ORIG,LONGITUDE_ORIG,TRASS,PARKING,SECURITY,CONDITIONING,INTERNET,PHONE_LINES,SERVICES,ROOM_STATE,VENTILATION,SEPARATE_ENTRANCE,
OWNERSHIP_TYPE) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

# Create a For loop to iterate through each row in the XLS file, starting at row 2 to skip the headers
for r in range(1, sheet.nrows):
    sub = sheet.cell(r,0).value
    ray = sheet.cell(r,1).value
    punkt = sheet.cell(r,2).value
    ter = sheet.cell(r,3).value
    ulica = sheet.cell(r,4).value
    dom = sheet.cell(r,5).value
    oren = sheet.cell(r,6).value
    seg = sheet.cell(r,7).value
    tip = sheet.cell(r,8).value
    naz = sheet.cell(r,9).value
    klass = sheet.cell(r,10).value
    cena = sheet.cell(r,11).value
    cena_chane = sheet.cell(r,12).value    
    pos = sheet.cell(r,13).value
    plosh = sheet.cell(r,14).value
    et = sheet.cell(r,15).value
    ets = sheet.cell(r,16).value
    god = sheet.cell(r,17).value
    opis = sheet.cell(r,18).value    
    ist = sheet.cell(r,19).value
    url = sheet.cell(r,20).value
    phone = sheet.cell(r,21).value
    lico = sheet.cell(r,22).value
    comp = sheet.cell(r,23).value
    mesto = sheet.cell(r,24).value
    mesto2 = sheet.cell(r,25).value
    metro = sheet.cell(r,26).value
    merto_min = sheet.cell(r,27).value
    oper = sheet.cell(r,28).value
    data = sheet.cell(r,29).value
    data2 = sheet.cell(r,30).value
    pars = sheet.cell(r,31).value
    kad = sheet.cell(r,32).value
    zag = sheet.cell(r,33).value
    sir = sheet.cell(r,34).value
    dol = sheet.cell(r,35).value
    try:
        tras = sheet.cell(r,36).value
    except IndexError:
        tras =''
    try:
        park = sheet.cell(r,37).value
    except IndexError:
        park =''
    try:
        ohr = sheet.cell(r,38).value
    except IndexError:
        ohr =''
    try:
        condey = sheet.cell(r,39).value
    except IndexError:
        condey =''
    try:
        inet = sheet.cell(r,40).value
    except IndexError:
        inet =''
    try:
        tel = sheet.cell(r,41).value
    except IndexError:
        tel=''
    try:
        usl = sheet.cell(r,42).value 
    except IndexError:
        usl=''
    try:
        otdel = sheet.cell(r,43).value
    except IndexError:
        otdel=''
    try:
        vint = sheet.cell(r,44).value
    except IndexError:
        vint =''
    try:
        vxod = sheet.cell(r,45).value
    except IndexError:
        vxod =''
    try:
        sobst = sheet.cell(r,46).value
    except IndexError:
        sobst =''
        
    
    
    
    print str(r)+' / '+str(sheet.nrows)
    
    # Assign values from each row
    values = (sub,ray,punkt,ter,ulica,dom,oren,seg,tip,naz,klass,cena,cena_chane,pos,plosh,et,ets,god,opis,ist,url,phone,lico,comp,mesto,mesto2,metro,merto_min,oper,data,data2,pars,kad,zag,sir,dol,tras,park,ohr,condey,inet,tel,usl,otdel,vint,vxod,sobst)

    # Execute sql Query
    cursor.execute(query, values)
    
    

# Close the cursor
cursor.close()

# Commit the transaction
database.commit()

# Close the database connection
database.close()

# Print results
print ""
print "All Done! Bye, for now."
print ""
columns = str(sheet.ncols)
rows = str(sheet.nrows)
print "I just imported "+ columns+  " columns and "  +rows+  " rows to MySQL!"
#raw_input(u'Введите число') 
raw_input('Press Enter to Exit!!')
