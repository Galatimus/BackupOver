# -*- coding: utf-8 -*-

# Scrapy settings for zillow project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html


BOT_NAME = 'zillow'

SPIDER_MODULES = ['zillow.spiders']
NEWSPIDER_MODULE = 'zillow.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 3

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
RANDOMIZE_DOWNLOAD_DELAY = True
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 1
#CONCURRENT_REQUESTS_PER_IP = 1
DOWNLOAD_TIMEOUT = 30


# Disable cookies (enabled by default)
#COOKIES_ENABLED = True
#COOKIES_DEBUG = True
# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
   'Accept-Encoding': 'gzip, deflate, br',
   'Referer':'https://www.google.com/',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    'zillow.middlewares.ZillowSpiderMiddleware': 543,
}
# Retry many times since proxies often fail
#RETRY_TIMES = 30
# Retry on most error codes since proxies fail for different reasons
#RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408,416]
# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620,    
}

# Proxy list containing entries like
# http://host1:port
# http://username:password@host2:port
# http://host3:port
# ...

#import requests
#def getProxyList():
    #resp = requests.get('https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt')
    #return resp.text.split()
#ROTATING_PROXY_LIST = getProxyList()


ROTATING_PROXY_LIST_PATH = '/home/oleg/pars/proxy/privat.txt'



#ROTATING_PROXY_LOGSTATS_INTERVAL = 1

# Proxy mode
# 0 = Every requests have different proxy
# 1 = Take only one proxy from the list and assign it to every requests
# 2 = Put a custom proxy to use in the settings
#PROXY_MODE = 2

# If proxy mode is 2 uncomment this sentence :
#CUSTOM_PROXY = 'http://181.215.79.142:22225' #US

#CUSTOM_PROXY = 'http://lum-customer-landly-zone-zone1:e7qhy6dhu0fs@zproxy.lum-superproxy.io:22225' #PL
#CUSTOM_PROXY = 'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt' 

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html

ITEM_PIPELINES = {'zillow.pipelines.MongoPipeline':300,}

#ITEM_PIPELINES = {
    #'zillow.pipelines.ZillowPipeline': 300,
#}

MONGO_URI = 'mongodb://Oleg:Ieijtycvr9dL@mongo.z.landly.ai:27017'
MONGO_DATABASE = 'landly'

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
