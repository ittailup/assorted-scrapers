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

class UnbounceSpider(Spider):
    name = 'unbounce'
    allowed_domains = ['unbounce.com']
    start_urls = ['http://careers.unbounce.com/']
    
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
        joblist = sel.xpath('//a[@class="lp-element lp-pom-button"]/span')
        #print joblist.extract()
        for jobs in joblist:
            listing = StartupJob()
            listing['startup'] = self.name
            listing['title'] = sel.xpath('//a[@class="lp-element lp-pom-button"]/span/text()').extract()[jobindex]
            listing['url'] = sel.xpath('//a[@class="lp-element lp-pom-button"]/@href').extract()[jobindex]
            #listing['location'] = sel.xpath("((//tr[@class='js-job-listing'])[" + str(jobindex) +"]/td)[2]/text()").extract()
            items.append(listing)
            jobindex += 1
        return items