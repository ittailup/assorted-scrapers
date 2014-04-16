from scrapy.contrib.spiders import XMLFeedSpider
from scrapy import signals
import logging
from scrapy.log import ScrapyFileLogObserver
from scrapy.xlib.pydispatch import dispatcher
from xmlanalyser.items import JobListing, FieldCounter
from scrapy import log
from collections import Counter

logfile = open('testlog.log', 'w')
log_observer = ScrapyFileLogObserver(logfile, level=logging.DEBUG)
log_observer.start()


class TestFeedSpider(XMLFeedSpider):    
    name = 'testfeed'
    allowed_domains = ['localhost']
    #start_urls = [l.strip() for l in open('test.txt').readlines()]
    start_urls = ["file:///Users/predius/adzuna.xml.1"]
                  
    #namespaces = [ ('sm', 'http://agora.com.pl/common/JobATO/domain'),]
    iterator = 'xml' # This is actually unnecessary, since it's the default value
    itertag = 'ad'
    
    
    elements =  {   'title':'title',
                    'jobid':'id',
                    'description':'content',
                    'requirements':'requirements',
                    'url':'url',
                    'company':'JobCompany',
                    'salary':'salary',
                    'city':'city',
                    'state':'region',
                    'category':'category'
                }
                    
    def __init__(self, stats):
        self.stats = stats
        self.titles_seen = []
        self.urls_seen = []
        self.indexes_seen = []
        self.jobids_seen = []
        self.count = 0 
        
        stats.set_value('all_dupes', 0)        
        stats.set_value('too_short', 0)        
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)
        
            
    def parse_node(self, response, node):
        log.msg('Hi, this is a <%s> node!: %s' % (self.itertag, ''.join(node.xpath('JobTitle/text()').extract())))
        #country = ''.join(node.xpath('country/text()').extract())
        #log.msg(country)
        item = JobListing()
        # set the xml values from the dictionary we give it
        for key in self.elements:
            item[key] = node.xpath("".join([self.elements[key],"/text()"])).extract()
            
        #item['url'] = url.xpath('sm:link/value/text()')
                # description append
        #item = self.build_description(node, item)
        #item = self.check_dupes(node, item)
        # create index by hashing head of title and description
        self.count = self.count+1
        return item
        
        
    
        
    def count_dupes(spider, reason):
        dupes = 0
        #for index in spider.index_counter:
           # dupes = dupes + spider.index_counter[str(index)]
        #log.msg("What")
        return dupes
            
        
    def spider_closed(spider, reason):
        spider.stats.set_value('count', spider.count)
        #print spider.index_counter
        #dupes = spider.count_dupes(spider)
                   
    
    def check_dupes(self, node, item):
        if item['title'] in self.titles_seen:
            item = self.discard(node, item, 'dupe_title')
        elif item['index'] in self.indexes_seen:
            item = self.discard(node, item, 'dupe_index')
        elif item['url'] in self.urls_seen:
            item = self.discard(node, item, 'dupe_url')
        elif item['jobid'] in self.jobids_seen:
            item = self.discard(node, item, 'dupe_ID')
        else:
            self.titles_seen.append(item['title'])
            self.indexes_seen.append(item['index'])
            self.urls_seen.append(item['url'])
            self.jobids_seen.append(item['jobid'])
        return item
        
        
    def get_hash(self,node,item):
        string = u"".join(item['description'])            
        #hashstring = "".join(map(str, [item.values()]))
        log.msg(string)
        hashstring = string[:100]
        log.msg("WHATTTTTTTT")
        index = hash(string)     
        return index
        
    def discard(self,node,item, reason):
        if 'too_short' in reason:
            item['discarded'] = 1
            short = self.stats.get_value('too_short')
            short += 1
            self.stats.set_value('too_short', short)
            item['reasondiscarded'] = "too_short"
        if 'dupe' in reason:
            item['discarded'] = 1
            item['reasondiscarded'] = reason
            dupesreason = self.stats.get_value(reason)
            dupes = self.stats.get_value('all_dupes')
            if bool(dupesreason):
                dupesreason += 1
                self.stats.set_value(reason, dupesreason)
            else:
                self.stats.set_value(reason, 1)
            dupes += 1
            self.stats.set_value("all_dupes", dupes)
        return item       
        
    def build_description(self, node, item):
        content = []
        contentelems = ['description']
        # get content from elements
        for w in contentelems:
            contentpath = "".join([w, "/text()"])
            content.append("".join(map(str, node.xpath(contentpath).extract())))
        # add content tags to single description
        contentstring = "".join(map(str, content))
        item['description'] = contentstring
        item['index'] = self.get_hash(node,item)
        log.msg("".join([contentstring,"wah"]))
        item['descriptionlength'] = len(contentstring)
        if item['descriptionlength'] < 100:
            reason = 'too_short'
            item = self.discard(node, item, reason)
        return item
        
        

        