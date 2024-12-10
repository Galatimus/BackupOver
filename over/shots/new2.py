#!/usr/bin/python
# -*- coding: utf-8 -*-



import math
import os
import time
import xlrd
import sys
import tempfile
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import TimeoutException,WebDriverException
from actual import get_actual

reload(sys)
sys.setdefaultencoding('utf-8')



def get_chrome_drive(driver_path=None):
    
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument('--hide-scrollbars')
    options.add_argument('--no-sandbox')
 
    driver = webdriver.Chrome(executable_path='D:\\VMF\\OlegPars\\webshot\\chromedriver\\chromedriver.exe',chrome_options=options,service_args=['--verbose'])
 
    return driver

def get_firefox_drive(driver_path=None):

    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')

    driver = webdriver.Firefox(executable_path=r'/usr/local/bin/geckodriver',firefox_options=options,service_log_path=None)

    return driver

def save_fullpage_screenshot(driver, url, output_path, tmp_prefix='selenium_screenshot', tmp_suffix='.png'):
   
    driver.get(url)
    time.sleep(2)
    shot = get_actual(driver,output_path)
    if shot == 'True':        
        window_height = driver.execute_script('return window.innerHeight')
        scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')
        num = int( math.ceil( float(scroll_height) / float(window_height) ) )            
        # get temp files
        tempfiles = []
        for i in range(num):
            fd,path = tempfile.mkstemp(prefix='{0}-{1:02}-'.format(tmp_prefix, i+1), suffix=tmp_suffix)
            os.close(fd)
            tempfiles.append(path)
            pass
        tempfiles_len = len(tempfiles)
    
        try:
            # take screenshots
            for i,path in enumerate(tempfiles):
                if i > 0:
                    driver.execute_script( 'window.scrollBy(%d,%d)' % (0, window_height) )
    
                driver.save_screenshot(path)
                pass
    
            # stitch images together
            stiched = None
            for i,path in enumerate(tempfiles):
                img = Image.open(path)
    
                w, h = img.size
                y = i * window_height
    
                if i == ( tempfiles_len - 1 ) and num > 1:
                    img = img.crop((
                        0,
                        h-(scroll_height % h),
                        w,
                        h
                    ))
    
                    w, h = img.size
                    pass
    
                if stiched is None:
                    stiched = Image.new('RGB', (w, scroll_height))
    
                stiched.paste(img, (
                    0, # x0
                    y, # y0
                    w, # x1
                    y + h # y1
                ))
                pass
            stiched.save(output_path)
            print '********************'
            print 'Ready ... ',output_path
            print '********************'
            return output_path
        finally:
            # cleanup
            for path in tempfiles:
                if os.path.isfile(path):
                    os.remove(path)
            pass
    else:
        print '-------------------------'
        print 'Not Actual >>> ',output_path
        print '--------------------------'

    


def main(url,filename):
    driver = get_firefox_drive()
    #driver = get_chrome_drive()

    driver.set_window_size(1024,800)
    try:
        save_fullpage_screenshot(driver,url,filename)
    except (TimeoutException,WebDriverException):
        driver.quit()
    
    driver.quit()
    time.sleep(1)
    return


if __name__ == '__main__':
    rb = xlrd.open_workbook(u'from/new-2.xlsx',on_demand=True)
    sheet = rb.sheet_by_index(0)
    for ak in range(0,sheet.nrows):
        print '******',ak,'/',str(sheet.nrows),'******'
        links = sheet.cell_value(ak,2)
        cod = '%d'%(sheet.cell_value(ak,0))
        ist = sheet.cell_value(ak,1).title().split('.')[0]
        filename = 'shot/'+ist+'_'+cod+'.png'
        try:
            main(links,filename)
        except (AttributeError,WebDriverException):
            continue 

    
    
    
