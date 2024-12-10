#!/usr/bin/python
# -*- coding: utf-8 -*-

def get_actual(driver,output_path):
    akt = ''
    name_ist = output_path.split('_')[0].replace('shot/','')
    #print name_ist
    if 'Youla' in name_ist:
        if u'Неактивно' in driver.title:
            akt = 'False'
        else:
            akt = 'True'
    elif 'Move' in name_ist:
        if driver.find_element_by_xpath(u'//p[@class="block-user__show-telephone_number"]') == None:
            akt = 'False'
        else:
            akt = 'True'
    elif 'Avito' in name_ist:
        if driver.find_element_by_xpath(u'//div[@class="item-phone js-item-phone"]/div') == None:
            akt = 'False'
        else:
            akt = 'True'
    elif 'Realtymag' in name_ist:
        if u'Запрошенная Вами страница была удалена' in driver.title:
            akt = 'False'
        else:
            akt = 'True'
    #***************************************************
    else:
        akt = 'True'
    return akt