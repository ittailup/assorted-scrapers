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

class ClioSpider(Spider):
    name = 'clio'
    allowed_domains = ['goclio.co.uk']
    start_urls = ['http://www.goclio.co.uk/careers/#currentopenings']
    
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
        joblist = sel.xpath('//div[@class="openings"]/div/div[@class="value"]/h5[@class="title"]/text()').extract()
        #print joblist.extract()
        for job in joblist:
            job = job.strip()
            if job:
                listing = StartupJob()
                listing['startup'] = self.name
                listing['title'] = job
                items.append(listing)
            #listing['location'] = sel.xpath("((//tr[@class='js-job-listing'])[" + str(jobindex) +"]/td)[2]/text()").extract()
            jobindex += 1
        return items