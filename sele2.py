#!/usr/bin/python
# -*- coding: utf-8 -*-



import datetime
import math
import time
import os
from selenium.common.exceptions import TimeoutException,WebDriverException,NoSuchElementException
import tempfile
from PIL import Image
from selenium import webdriver


def get_chrome_drive(driver_path=None):
    
 
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument('--hide-scrollbars')
    options.add_argument('--no-sandbox')
 
    driver = webdriver.Chrome(executable_path='D:\\VMF\\OlegPars\\webshot\\chromedriver\\chromedriver.exe',chrome_options=options,service_args=['--verbose'])
 
    return driver


def save_fullpage_screenshot(driver, url, output_path, tmp_prefix='selenium_screenshot', tmp_suffix='.png'):
    """
    Creates a full page screenshot using a selenium driver by scrolling and taking multiple screenshots,
    and stitching them into a single image.
    """

    # get the page
    try:
        driver.get(url)
    except (TimeoutException,WebDriverException):
        pass    

    # get dimensions
    window_height = driver.execute_script('return window.innerHeight')
    scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')
    num = int(math.ceil(float(scroll_height) / float(window_height)))

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


def main():
    #now = datetime.datetime.now()

    #filename = 'shot/screenshot-{}-{}.png'.format(
        #now.strftime('%Y%m%d'),
        #now.strftime('%H%M%S')
    #)
    l= open('urls.txt').read().splitlines()
    
    driver = get_chrome_drive()

    driver.set_window_size(1280,800)

    #url = 'https://www.avito.ru/moskva/kommercheskaya_nedvizhimost/ofis._profsoyuznaya_25a._103m2_1477055574'
    
    for p in range(637,len(l)):
        print '******',p,'/',len(l),'******'
        filename = 'shot/screen_'+str(p)+'.png'
        time.sleep(2) 
        driver.get("about:blank")  
        time.sleep(3) 
        save_fullpage_screenshot(driver,l[p],filename)
        print filename
    driver.quit()



if __name__ == '__main__':
    main()
