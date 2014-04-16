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

class YouilabsSpider(Spider):
    name = 'youilabs'
    allowed_domains = ['youilabs.com']
    start_urls = ['http://youilabs.com/who-we-are/working-at-youi/']
    
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
        joblist = sel.xpath('//div[@class="careertext"]/div/a').extract()
        #print joblist.extract()
        for job in joblist:
            listing = StartupJob()
            listing['startup'] = self.name
            listing['title'] = sel.xpath('//div[@class="careertext"]/div/a/h2/text()').extract()[jobindex]
            listing['url'] = sel.xpath('//div[@class="careertext"]/div/a/@href').extract()[jobindex]
            items.append(listing)
            #listing['location'] = sel.xpath("((//tr[@class='js-job-listing'])[" + str(jobindex) +"]/td)[2]/text()").extract()
            jobindex += 1
        return items