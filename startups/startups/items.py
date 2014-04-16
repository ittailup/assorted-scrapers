# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class Startup(Item):
    # define the fields for your item here like:
    # name = Field()
    name = Field()
    industry = Field()
    totaljobs = Field()
    pass
    
class StartupJob(Item):
    startup = Field()
    category = Field()
    title = Field()
    url = Field()
    location = Field()
    pass
