# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QVCItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    beforePrice = scrapy.Field()
    Price = scrapy.Field()
    number =scrapy.Field()
    url = scrapy.Field()
    day = scrapy.Field()
    startTime = scrapy.Field()
    endTime = scrapy.Field()
    description = scrapy.Field()
    show = scrapy.Field()
    show_description = scrapy.Field()
    pass

class QVCDailyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    beforePrice = scrapy.Field()
    Price = scrapy.Field()
    number =scrapy.Field()
    url = scrapy.Field()
    day = scrapy.Field()
    time = scrapy.Field()
    description = scrapy.Field()
    show = scrapy.Field()
    show_description = scrapy.Field()
    pass

class QVCUKItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    beforePrice = scrapy.Field()
    Price = scrapy.Field()
    number =scrapy.Field()
    url = scrapy.Field()
    day = scrapy.Field()
    time = scrapy.Field()
    description = scrapy.Field()
    show = scrapy.Field()
    show_description = scrapy.Field()
    pass