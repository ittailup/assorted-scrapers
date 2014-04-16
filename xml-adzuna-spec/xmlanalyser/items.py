# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class JobListing(Item):
    # define the fields for your item here like:
    # name = Field()
    title = Field()
    index = Field()
    description = Field()
    descriptionlength = Field()
    requirements = Field()
    jobid = Field()
    url = Field()
    city = Field()
    state = Field()
    location = Field()
    country = Field()
    country = Field()
    category = Field()
    company = Field()
    salary = Field()
    date = Field()
    expirydate = Field()
    discarded = Field()
    reasondiscarded = Field()
    contracttype = Field()
    
    pass

class FieldCounter(Item):
    fieldname = Field()
    fieldtype = Field()
    count = Field()