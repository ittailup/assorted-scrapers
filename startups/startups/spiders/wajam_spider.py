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

class WajamSpider(Spider):
    name = 'wajam'
    allowed_domains = ['wajam.com']
    start_urls = ['http://www.wajam.com/careers/jobs']
    
    def __init__(self, stats):
        self.stats = stats
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)
    
    
    def parse(self, response):
        sel = Selector(response)
        categories = sel.xpath("//h3/text()").extract()
        
        items = []
        jobindex = 0
        joblist = sel.xpath("//div[@class='joblinks']")
        #print joblist.extract()
        for jobs in joblist:
            listing = StartupJob()
            listing['startup'] = response.url
            listing['title'] = sel.xpath("//div[@class='joblinks']/a/text()").extract()[jobindex]
            listing['url'] = sel.xpath("//div[@class='joblinks']/a/@href").extract()[jobindex]
            #listing['category'] = sel.xpath("//span[@class='resumator_department']/text()").extract()[jobindex]
            #listing['location'] = sel.xpath("((//tbody/tr)["+ str(jobindex+1)+ "]/td)[2]/text()").extract()
            items.append(listing)
            jobindex += 1
        return items