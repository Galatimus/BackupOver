#!/usr/bin/python
# -*- coding: utf-8 -*-




import os
import time
import xlrd
import random
import urllib3
import sys
from selenium import webdriver
from selenium.common.exceptions import TimeoutException,WebDriverException
from selenium.webdriver.common.proxy import *
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


reload(sys)
sys.setdefaultencoding('utf-8')





def get_firefox_drive(driver_path=None):
    
    
    #PROXY = random.choice(list(open('../../tipa.txt').read().splitlines()))
    #myproxy = random.choice(list(open('../../ivan.txt').read().splitlines())).split(':Ivan')[0]
    #DesiredCapabilities.PHANTOMJS['phantomjs.page.settings.userAgent'] = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0"    
    ua = dict(DesiredCapabilities.PHANTOMJS)
    #print myproxy
    ua["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0"
    driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any', '--web-security=false'],service_log_path=None)


    #options = webdriver.FirefoxOptions()
    #options.add_argument('-headless')
    
    #driver = webdriver.Firefox(executable_path=r'/usr/local/bin/geckodriver',firefox_profile=profile,firefox_options=options,service_log_path=None)
    
    return driver

def save_fullpage_screenshot(driver, url, output_path):
    akt = 0
    name_ist = output_path.split('_')[0].replace('shot/','')
    driver.get(url)
    #print name_ist
    time.sleep(2)
    #***************************************************
    if 'Youla' in name_ist:
        if u'Неактивно' in driver.title:
            akt = 0
        else:
            akt = 1
    elif 'Move' in name_ist:
        if driver.find_element_by_xpath(u'//p[@class="block-user__show-telephone_number"]') == None:
            akt = 0
        else:
            akt = 1
    elif 'Avito' in name_ist:
        if driver.find_element_by_xpath(u'//div[@class="item-phone js-item-phone"]/div') == None:
            akt = 0
        else:
            akt = 1
    elif 'Realtymag' in name_ist:
        if u'Запрошенная Вами страница была удалена' in driver.title:
            akt = 0
        else:
            akt = 1
    #***************************************************
   
    #---------------------------------------------------------
    if akt == 1:
        print 'OK >> ',driver.current_url
        driver.execute_script('document.body.style.background = "white"')
        driver.save_screenshot(output_path)
        print 'Ready ... ',output_path
        return output_path
    else:
        print 'Not Actual >>> ',output_path

def main(url,filename):
    driver = get_firefox_drive()
    #driver = get_chrome_drive()

    driver.set_window_size(1024,800)
    #driver.set_page_load_timeout(10)
    #driver.set_script_timeout(10)    
    try:
        save_fullpage_screenshot(driver,url,filename)
    except (TimeoutException,WebDriverException):
        driver.close()
    
    driver.close()
    time.sleep(1)
    return


if __name__ == '__main__':
    rb = xlrd.open_workbook(u'new-1.xlsx',on_demand=True)
    sheet = rb.sheet_by_index(0)
    for ak in range(1,sheet.nrows):
        print '******',ak,'/',str(sheet.nrows),'******'
        links = sheet.cell_value(ak,2)
        cod = '%d'%(sheet.cell_value(ak,0))
        ist = sheet.cell_value(ak,1).title().split('.')[0]
        filename = 'shot/'+ist+'_'+cod+'.png'
        try:
            main(links,filename)
        except (WebDriverException,urllib3.exceptions.MaxRetryError,urllib3.exceptions.ProtocolError):
            continue

    
    
    
