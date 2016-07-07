# -*- coding: utf-8 -*-
import scrapy

from QVCscrape.items import QVCItem
from scrapy.linkextractors import LinkExtractor
from igraph import *


class QVCSpider(scrapy.Spider):
	name = "QVC"
	allowed_domains = ["qvc.com"]
	start_urls = ["http://www.qvc.com/webapp/wcs/stores/servlet/ProgramGuideDailyView?TimeZoneSelect=EST&cm_sp=24Hr-_-HEAD-_-Desc&cm_re=MH-_-SHOPQVCLIVE-_-PROGRAMGUIDE&storeId=10251&catalogId=10151&langId=-1&Navigate=20160707&channelCode=QVC"]


	def parse(self, response):

		#iterate over links
		#for sel in response.xpath('//@href'):
		for sel in response.xpath('//div[@class="divSeeItems"]'):
			link = sel.xpath('a/@href').extract()
			url = response.urljoin(link)
			request = scrapy.Request(url, self.day_page)
			yield request


		# for sel in response.xpath('//@href'):
		# 	item = DmozItem()
		# 	item['title'] = sel.xpath('a/text()').extract()
		# 	item['link']=link = sel.xpath('a/@href').extract()
		# 	item['desc'] = sel.xpath('text()').extract()
		# 	print item['link']

	#follow links recursively until no unique links exist
	def day_page(self,response):
		links = LinkExtractor(allow=self.allowed_domains, deny=()).extract_links(response)
		for sel in links:
			request = scrapy.Request(node['link'], self.follow_the_trail)
			yield request

	def closed(self, reason):
		pass
		

    	
