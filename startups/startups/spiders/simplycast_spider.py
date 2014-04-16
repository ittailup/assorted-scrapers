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

class SimplyCastSpider(Spider):
    name = 'simplycast'
    allowed_domains = ['www.simplycast.com']
    start_urls = ['http://www.simplycast.com/about-us/overview/career-opportunities/']
    
    def __init__(self, stats):
        self.stats = stats
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)
    
    
    def parse(self, response):
        sel = Selector(response)
        jobs = sel.xpath("//div[@class='entry-content']/p/a")
        
        items = []
        index = 0
        for job in jobs:
            listing = StartupJob()
            listing['title'] = sel.xpath("//div[@class='entry-content']/p/a/text()").extract()[index]
            listing['url'] = sel.xpath("//div[@class='entry-content']/p/a/text()").extract()[index]
            items.append(listing)
            index += 1
        return items
            
            
            
        