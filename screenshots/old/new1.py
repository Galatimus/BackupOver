#!/usr/bin/python
# -*- coding: utf-8 -*-



import math
import os
import time
import xlrd
import random
import sys
import tempfile
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import TimeoutException,WebDriverException
from selenium.webdriver.common.proxy import *
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


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
    
    
    PROXY = random.choice(list(open('../../tipa.txt').read().splitlines()))
    ua = dict(DesiredCapabilities.PHANTOMJS)
    ua["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0")
    driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'],service_log_path=None)


    #options = webdriver.FirefoxOptions()
    #options.add_argument('-headless')
    
    #driver = webdriver.Firefox(executable_path=r'/usr/local/bin/geckodriver',firefox_profile=profile,firefox_options=options,service_log_path=None)

    return driver

def save_fullpage_screenshot(driver, url, output_path, tmp_prefix='selenium_screenshot', tmp_suffix='.png'):
    """
    Creates a full page screenshot using a selenium driver by scrolling and taking multiple screenshots,
    and stitching them into a single image.
    """

    # get the page
    
    driver.get(url)
    time.sleep(2)
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
    finally:
        # cleanup
        for path in tempfiles:
            if os.path.isfile(path):
                os.remove(path)
        pass

    return output_path


def main(url,filename):
    driver = get_firefox_drive()
    #driver = get_chrome_drive()

    driver.set_window_size(1024,800)
    try:
        save_fullpage_screenshot(driver,url,filename)
    except (TimeoutException,WebDriverException):
        driver.quit()
    
    driver.close()
    time.sleep(1)
    print '********************'
    print 'Ready ... ',filename
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
        except WebDriverException:
            continue

    
    
    
