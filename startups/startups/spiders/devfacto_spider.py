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

class ResumatorSpider(Spider):
    name = 'devfacto'
    allowed_domains = ['devfacto.com']
    start_urls = ['http://www.devfacto.com/careers/']
    
    def __init__(self, stats):
        self.stats = stats
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)
    
    
    def parse(self, response):
        sel = Selector(response)
        #categories = sel.xpath("//h3/text()").extract()
        
        items = []
        jobindex = 0
        joblist = sel.xpath("//tbody/tr")
        #print joblist.extract()
        for jobs in joblist:
            listing = StartupJob()
            listing['startup'] = response.url
            listing['title'] = sel.xpath("((//tbody/tr)["+ str(jobindex) +"]/td)[1]/a/text()").extract()
            listing['url'] = sel.xpath("((//tbody/tr)["+ str(jobindex) +"]/td)[1]/a/@href").extract()
            listing['location'] = sel.xpath("((//tbody/tr)["+ str(jobindex) +"]/td)[2]/text()").extract()
            items.append(listing)
            jobindex += 1
        return items