#!/usr/bin/python
# -*- coding: utf-8 -*-





from grab.spider import Spider,Task
import grab.spider.queue_backend
import grab.spider.queue_backend.memory
import grab.transport
import grab.transport.curl
import logging
import time
import xlrd
import os
import re
from datetime import datetime
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


   
logging.basicConfig(level=logging.DEBUG)

       
name ='0616'

class Gis(Spider):
       
       
       def prepare(self):
              self.rb = xlrd.open_workbook(name+'.xlsx',on_demand=True)
              self.sheet = self.rb.sheet_by_index(0)              
              self.workbook = xlsxwriter.Workbook(u'Актуальность_.xlsx')#+datetime.today().strftime('%d.%m.%Y')+'.xlsx')
              self.ws = self.workbook.add_worksheet()
              self.ws.write(0,0, u"КодПредложения")
              self.ws.write(0,1, u"Источник")
              self.ws.write(0,2, u"Ссылка")
              self.ws.write(0,3, u"Актуальность")
              self.row= 1  

              
       def task_generator(self):
              for ak in range(1,self.sheet.nrows):
                     #time.sleep(1)
                     links = self.sheet.cell_value(ak,2).strip()
                     cod = self.sheet.cell_value(ak,0).strip()
                     ist = self.sheet.cell_value(ak,1).strip()
                     prov = self.sheet.cell_value(ak,1).split(' (')[1].replace(')','').strip()
                     yield Task ('post',url= links,refresh_cache=True,ist=ist,cod=cod,prov=prov,network_try_count=100)
        
                     
       def task_post(self,grab,task):
              print task.url,task.prov
              
              if 'AVITO' in task.ist:
                     akt = grab.doc.select(u'//div[@class="item-phone js-item-phone"]/div').exists()
                     
             
              
              
              
              
             ##if 'Domofond' in opcs:
              #if 'domofond.ru/' in task.url:
                     #if grab.doc.select(u'//a[@class="b-btn m-green g-size-lg"]/@data-url').exists() == True:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')        
       
       
              #elif 'yuga.ru/' in task.url:
                     #if grab.doc.select(u'//div[@itemprop="description"]').exists() == True:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
       
       
              #elif 'dom.59.ru/' in task.url:
                     #if grab.doc.select(u'//a[@class="all_ads_user_link"]').exists() == True:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')        
       
              ##if '45_ru' in opcs:       
              #elif 'dom.45.ru/' in task.url:
                     #if grab.doc.select(u'//a[@class="all_ads_user_link"]').exists() == True:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
       
       
              ##if '72_ru' in opcs:       
              #elif 'dom.72.ru/' in task.url:
                     #if grab.doc.select(u'//a[@class="all_ads_user_link"]').exists() == True:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
       
              ##if 'Domchel_ru' in opcs:        
              #elif 'domchel.ru/' in task.url:
                     #if grab.doc.select(u'//a[@class="all_ads_user_link"]').exists() == True:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
       
              ##if 'Farpost' in opcs: 
              #elif 'farpost.ru/' in task.url:
                     #if grab.doc.select(u'//strong[contains(text(),"Объявление находится в архиве и может быть неактуальным.")]').exists() == True:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = datetime.today().strftime('%d.%m.%Y')
       
              ##if 'Infoline' in opcs:
              #elif 'vrx.ru/' in task.url:
                     #if grab.doc.select(u'//td[contains(text(),"Операция:")]/following-sibling::td').exists() == True:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
       
       
              ##if 'Tulahouse_ru' in opcs:
              #elif 'tulahouse.ru/' in task.url:
                     #if grab.doc.select(u'//p[@class="item-description"]').exists() == True:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
                            
              #elif 'kalugahouse.ru/' in task.url:
                     #if grab.doc.select(u'//p[@class="item-description"]').exists() == True:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
                            
              #elif 'vladimirhouse.ru/' in task.url:
                     #if grab.doc.select(u'//p[@class="item-description"]').exists() == True:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')                            
       
              ##if 'ГдеЭтотДом' in opcs:
              #elif 'gdeetotdom.ru/' in task.url:
                     #if grab.doc.select(u'//div[@class="adv_status"]').exists() == True:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = datetime.today().strftime('%d.%m.%Y')
       
              ##if 'Недвижимость_Астрахани' in opcs:
              #elif 'n30' in task.url :
                     #if grab.doc.select(u'//td[@class="thprice"]').exists() == True:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
       
              ##if 'Недвижимость_Екатеринбурга' in opcs:
              #elif 'kvadrat66.ru/' in task.url:
                     #if grab.doc.select(u'//td[@class="thprice"]').exists() == True:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
       
              ##if 'Недвижимость_Кемерово' in opcs:
              #elif 'kemdom.ru/' in task.url:
                     #if grab.doc.select(u'//td[@class="thprice"]').exists() == True:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
       
              ##if 'Недвижимость_Саратова' in opcs:
              #elif 'kvadrat64.ru/' in task.url:
                     #if grab.doc.select(u'//td[@class="thprice"]').exists() == True:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
       
       
              ##if 'Недвижимость_и_цены' in opcs:
              #elif 'dmir.ru/' in task.url:
                     #if grab.doc.select(u'//span[@id="price_offer"]').exists() == True:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
       
              ##if 'Росриэлт_Недвижимость' in opcs:
              #elif 'rosrealt.ru/' in task.url:
                     #if grab.doc.select(u'//div[@class="section_right"]').exists() == True:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
       
              ##if 'Уральская_палата_недвижимости' in opcs:
              #elif 'upn.ru/' in task.url:
                     #if grab.doc.select(u'//div[@id="ctl00_VOI_pnError"]').exists() == True:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = datetime.today().strftime('%d.%m.%Y')
       
              ##if 'Циан' in opcs:
              #elif 'cian.ru/' in task.url:
                     #if grab.doc.select(u'//span[@class="object_descr_warning object_descr_warning_red"]').exists() == True:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = datetime.today().strftime('%d.%m.%Y')
       
              ##if 'Avito' in opcs:
              #elif 'avito.ru/' in task.url:
                     #if grab.doc.select(u'//div[@class="item-phone js-item-phone"]/div').exists() == True:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
       
       
              ##if 'IRR' in opcs:
              #elif 'irr.ru/' in task.url:
                     #if grab.doc.select(u'//@data-phone').exists() == True:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')                    
       
       
              ##if 'Mirkvartir' in opcs:
              #elif 'mirkvartir.ru/' in task.url:
                     #if grab.doc.select(u'//span[@class="phones"]').exists() == True:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')                     
       
              ##if 'Theproperty' in opcs:
              #elif 'theproperty.ru/' in task.url:
                     #if grab.doc.select(u'//p[@class="archive"]').exists() == True:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = datetime.today().strftime('%d.%m.%Y')                     
       
              ##if 'RealtyMag' in opcs:
              #elif 'realtymag.ru/' in task.url:
                     #if grab.doc.select(u'//div[@class="error-page__code"]').exists() == True:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = datetime.today().strftime('%d.%m.%Y')                     
       
       
              ##if 'Необходимая_недвижимость' in opcs:
              #elif 'nndv.ru/' in task.url:
                     #if grab.doc.select(u'//td[@class="paddLR5TB2"]').exists() == True:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')                     
       
              ##if 'Mlsn' in opcs:
              #elif 'mlsn.ru/' in task.url:
                     #if grab.doc.select(u'//div[@class="NotFound__base"]').exists() == True:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = datetime.today().strftime('%d.%m.%Y')                     
       
              #elif 'life-realty.ru/' in task.url :
                     #if grab.response.code ==200:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
       
              #elif 'citystar.ru/' in task.url:
                     #if grab.response.code ==200:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
       
              #elif 'citystar74.ru/' in task.url:
                     #if grab.response.code ==200:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
       
              #elif 'realtyekaterinburg.ru/' in task.url:
                     #if grab.response.code ==200:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')                        
       
              #elif 'n1.ru/' in task.url:
                     #if grab.response.code ==200:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
       
              #elif 'rosnedv.ru/' in task.url:
                     #if grab.response.code ==200:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
       
              #elif 'ayax.ru/' in task.url:
                     #if grab.response.code ==200:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
       
              #elif 'qp.ru/' in task.url:
                     #if grab.doc.select(u'//div[@class="contacts-info contacts-phones"]').exists() == True:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')                            
       
              #elif 'doska.ru/' in task.url:
                     #if grab.doc.select(u'//span[@id="phone_td_1"]').exists() == True:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
       
              #elif 'ners.ru/' in task.url:
                     #if grab.doc.select(u'//div[@class="notes_publish_status"]').exists() == True:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = datetime.today().strftime('%d.%m.%Y')
       
              #elif 'ngs.ru/' in task.url:
                     #if grab.doc.select(u'//div[@class="card__phones-container"]').exists() == True:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
       
              #elif 'bn.ru/' in task.url:
                     #if grab.doc.select(u'//dt[contains(text(),"Телефон")]').exists() == True:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
       
              #elif 'nmls.ru/' in task.url:
                     #if grab.doc.select(u'//div[@class="mb10"]').exists() == True:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')                            
       
              #elif 'bkn42.ru/' in task.url:
                     #nek = grab.doc.select(u'//title').text().split(' ')[0]
                     #if nek == u'ПРОДАНО':
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
                     #elif nek ==u'СДАНО':
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = datetime.today().strftime('%d.%m.%Y')
       
              #elif 'realtyvision.ru/' in task.url:
                     #if grab.response.code ==200:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
       
              #elif 'dom43.ru/' in task.url:
                     #if grab.response.code ==200:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
                            
              #elif 'irk.ru/' in task.url:
                     #if grab.response.code ==200:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')                            
       
              #elif 'rk-region.ru/' in task.url:
                     #if grab.response.code ==200:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')    
              #elif 'home29.ru/' in task.url:
                     #if grab.doc.select(u'//div[@class="message"]').exists() == True:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = datetime.today().strftime('%d.%m.%Y')
       
       #############################Nedvizhka.RU############################################################
       
              #elif 'ned22.ru/' in task.url:
                     #if grab.response.code ==200:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y') 
       
              #elif 'eest.ru/' in task.url:
                     #if grab.response.code ==200:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
       
              #elif 'ned30.ru/' in task.url:
                     #if grab.response.code ==200:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
       
              #elif 'ned31.ru/' in task.url:
                     #if grab.response.code ==200:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
       
              #elif 'ned33.ru/' in task.url:
                     #if grab.response.code ==200:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
       
              #elif 'nedvizhka.ru/' in task.url:
                     #if grab.response.code ==200:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
       
              #elif 'vnk39.ru/' in task.url:
                     #if grab.response.code ==200:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
       
              #elif 'radver.ru/' in task.url:
                     #if grab.response.code ==200:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
       
              #elif '23estate.ru/' in task.url:
                     #if grab.response.code ==200:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
       
              #elif 'ned77.ru/' in task.url:
                     #if grab.response.code ==200:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y') 
       
              #elif 'ned74.ru/' in task.url:
                     #if grab.response.code ==200:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
       
              #elif '52metra.ru/' in task.url:
                     #if grab.response.code ==200:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
       
              #elif 'prmrealty.ru/' in task.url:
                     #if grab.response.code ==200:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
       
              #elif 'ned02.ru/' in task.url:
                     #if grab.response.code ==200:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
       
              #elif 'ned61.ru/' in task.url:
                     #if grab.response.code ==200:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
       
              #elif 'realt66.ru/' in task.url:
                     #if grab.response.code ==200:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
                            
              #elif 'base.zem.ru/' in task.url:
                     #if grab.doc.select(u'//span[contains(text(),"Телефон:")]/following-sibling::span').exists() == True:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
                            
              #elif 'dom.vse42.ru/' in task.url:
                     #if grab.response.code ==200:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
                            
              #elif 'brsn.ru/' in task.url:
                     #if grab.response.code ==200:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
                            
              #elif 'bizzona.ru/' in task.url:
                     #if grab.response.code ==200:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
                            
              #elif 'businessesforsale.ru/' in task.url:
                     #if grab.response.code ==200:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
                            
              #elif 'bbport..ru/' in task.url:
                     #if grab.response.code ==200:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')                            
                            
              #elif 'business-asset.ru/' in task.url:
                     #if grab.response.code ==200:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
                            
              #elif 'delomart.ru/' in task.url:
                     #if grab.response.code ==200:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
                            
              #elif 'alterainvest.ru/' in task.url:
                     #if grab.response.code ==200:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')
                            
              #elif 'biztorg.ru/' in task.url:
                     #if grab.response.code ==200:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')                            
                            
              #elif 'bizprodan.ru/' in task.url:
                     #if grab.response.code ==200:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')                            
                            
              #elif '62.76.186.115/' in task.url:
                     #if grab.response.code ==200:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')                            
                            
              #elif 'roszem.ru/' in task.url:
                     #if grab.doc.select(u'//dt[contains(text(),"Телефон")]/following-sibling::dd').exists() == True:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')                            
       
              #elif 'ned72.ru/' in task.url:
                     #if grab.response.code ==200:
                            #akt = datetime.today().strftime('%d.%m.%Y')
                     #else:
                            #akt = u'Снят'+' '+datetime.today().strftime('%d.%m.%Y')                
              #else:
                     #akt =''
                     
                     
                     
                     
              self.ws.write(self.row, 1, akt)
              self.ws.write_string(self.row, 0, task.url)
              self.ws.write_string(self.row, 2, task.ist)
              print('*'*50)
              print akt
              print 'Ready - '+str(self.row)+'/'+str(self.sheet.nrows)
              print 'Tasks - %s' % self.task_queue.size()
              print('*'*50) 
              self.row+= 1              
                     
              if self.row > 100:
                     self.stop()                      
              
              
bot = Gis(thread_number=3, network_try_limit=1000)
bot.load_proxylist('../tipa.txt','text_file')
bot.create_grab_instance(timeout=5000, connect_timeout=5000)
bot.run()
print('Wait 2 sec...')
time.sleep(2)
print('Save it...')    
command = 'mount -t cifs //192.168.1.6/d /home/oleg/pars -o username=oleg,password=1122,_netdev,rw,iocharset=utf8,file_mode=0777,dir_mode=0777' #'mount -a -O _netdev'
#command = 'apt autoremove'
p = os.system('echo %s|sudo -S %s' % ('1122', command))
print p
time.sleep(1)
bot.workbook.close()
#workbook.close()
print('Done!')

