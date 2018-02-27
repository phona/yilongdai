# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YilongdaiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	detailsTitle = scrapy.Field()
	time = scrapy.Field()
	index = scrapy.Field()
	tid = scrapy.Field()
	amount = scrapy.Field()
	phases = scrapy.Field()
	progressBar = scrapy.Field()
	authod_userName = scrapy.Field()
	authod_userId = scrapy.Field()
	interestrate = scrapy.Field()
	create_time = scrapy.Field()
