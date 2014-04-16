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

class TechvibesSpider(Spider):
    name = 'techvibes'
    allowed_domains = ['techvibes.com']
    start_urls = ["http://www.techvibes.com/job/global/company/payfirma-corporation",
                "http://www.techvibes.com/job/global/company/freshbooks",
                'http://www.techvibes.com/job/global/company/top-hat',
                'http://www.techvibes.com/job/global/company/trulioo',
                'http://www.techvibes.com/job/global/company/hootsuite']
    
    def __init__(self, stats):
        self.stats = stats
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)
    
    
    def parse(self, response):
        sel = Selector(response)
    
        items = []
        jobindex = 0
        joblist = sel.xpath('//h2[@class="linked-heading"]/a')
        #print joblist.extract()
        for jobs in joblist:
            listing = StartupJob()
            listing['startup'] = sel.xpath('//h1[@class="padding-b10"]/text()').extract()[0].strip()
            listing['title'] = sel.xpath('//h2[@class="linked-heading"]/a/text()').extract()[jobindex]
            listing['url'] = sel.xpath('//h2[@class="linked-heading"]/a/@href').extract()[jobindex]
            #listing['category'] = sel.xpath("//span[@class='resumator_department']/text()").extract()[jobindex]
            #listing['location'] = sel.xpath("((//tbody/tr)["+ str(jobindex+1)+ "]/td)[2]/text()").extract()
            items.append(listing)
            jobindex += 1
        return items