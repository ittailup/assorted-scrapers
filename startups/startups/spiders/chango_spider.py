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
    name = 'chango'
    allowed_domains = ['chango.com']
    start_urls = ['file:///Users/predius/Desktop/chango.html']
    
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
        joblist = sel.xpath("//div[@class='panel-heading']")
        #print joblist.extract()
        for jobs in joblist:
            listing = StartupJob()
            listing['startup'] = 'Chango'
            listing['title'] = sel.xpath("//div[@class='col-md-5']/div/text()").extract()[jobindex]
            listing['url'] = sel.xpath("//div[@class='panel-heading']/a/@href").extract()[jobindex]
            listing['location'] = sel.xpath("//div[@class='col-md-3']/div/text()").extract()[jobindex]
            items.append(listing)
            jobindex += 1
        return items