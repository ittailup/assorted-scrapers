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

class MobifySpider(Spider):
    name = 'mobify'
    allowed_domains = ['jobscore.com']
    start_urls = ['http://www.jobscore.com/jobs2/mobify?sid=68']
    
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
        joblist = sel.xpath("//tr[@class='js-job-listing']")
        #print joblist.extract()
        for jobs in joblist:
            listing = StartupJob()
            listing['startup'] = response.url
            listing['title'] = sel.xpath("(//tr[@class='js-job-listing'])[" + str(jobindex) +"]/td/a/text()").extract()
            listing['url'] = sel.xpath("(//tr[@class='js-job-listing'])[" + str(jobindex) +"]/td/a/@href").extract()
            listing['location'] = sel.xpath("((//tr[@class='js-job-listing'])[" + str(jobindex) +"]/td)[2]/text()").extract()
            items.append(listing)
            jobindex += 1
        return items