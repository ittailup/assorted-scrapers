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

class OutpostSpider(Spider):
    name = 'outpost'
    allowed_domains = ['outpost.travel']
    start_urls = ["https://outpost.travel/#!/jobs"]
    
    def __init__(self, stats):
        self.stats = stats
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)
    
    
    def parse(self, response):
        sel = Selector(response)
    
        items = []
        jobindex = 0
        joblist = sel.xpath('//div[@class="accordion"]/div/div/a')
        #print joblist.extract()
        for jobs in joblist:
            listing = StartupJob()
            listing['startup'] = self.name
            listing['title'] = sel.xpath('//div[@class="accordion"]/div/div/a/b/text()').extract()[jobindex]
            listing['url'] = response.url #sel.xpath('//div[@class="accordion"]/div/div/a/@href').extract()[jobindex]
            #listing['category'] = sel.xpath("//span[@class='resumator_department']/text()").extract()[jobindex]
            #listing['location'] = sel.xpath("((//tbody/tr)["+ str(jobindex+1)+ "]/td)[2]/text()").extract()
            items.append(listing)
            jobindex += 1
        return items