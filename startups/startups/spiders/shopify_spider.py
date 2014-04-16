from scrapy.spider import Spider
from scrapy import signals
from scrapy.selector import Selector
import logging
import csv
from startups.items import Startup, StartupJob
from scrapy.log import ScrapyFileLogObserver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import log

logfile = open('testlog.log', 'w')
log_observer = ScrapyFileLogObserver(logfile, level=logging.DEBUG)
log_observer.start()

class ShopifySpider(Spider):
    name = 'shopify'
    allowed_domains = ['www.shopify.ca']
    start_urls = ['http://www.shopify.ca/careers']
    
    def __init__(self, stats):
        self.stats = stats
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)
    
    
    def parse(self, response):
        sel = Selector(response)
        joblists = sel.xpath("//ul[@class='job-list']")
        
        for category in joblists:
            log.msg(sel.xpath('//a'))
        