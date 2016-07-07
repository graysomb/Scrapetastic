# -*- coding: utf-8 -*-
import scrapy

from QVCscrape.items import QVCItem
from scrapy.linkextractors import LinkExtractor
from igraph import *


class QVCSpider(scrapy.Spider):
	visited_urls=[]
	name = "QVC"
	allowed_domains = ["qvc.com"]
	start_urls = ["http://www.qvc.com/webapp/wcs/stores/servlet/ProgramGuideWeeklyView?storeId=10251&TimeZoneSelect=EST&weekRange=0&channelCode=QVC"]


	def parse(self, response):

		#iterate over links
		for sel in response.xpath('//div[@class="divSeeItems"]'):
			link = sel.xpath('a/@href').extract()
			url = response.urljoin(link[0])
			if (self.isUnique(url)):
				self.visited_urls.append(url)
				request = scrapy.Request(url, self.day_page)
				yield request


		# for sel in response.xpath('//@href'):
		# 	item = DmozItem()
		# 	item['title'] = sel.xpath('a/text()').extract()
		# 	item['link']=link = sel.xpath('a/@href').extract()
		# 	item['desc'] = sel.xpath('text()').extract()
		# 	print item['link']

	#follow day page links
	def day_page(self,response):
		daySel = response.xpath('//option[@value=""]')
		day = daySel.xpath('text()').extract()

		#save day and send as meta response stuff
		if len(day)>0:
			day = day[0]

		for sel in response.xpath('//a[@class="prodDetailLink url"]'):
			link = sel.xpath('@href').extract()
			url = response.urljoin(link[0])



		# for sel in links:
		# 	request = scrapy.Request(node['link'], self.follow_the_trail)
		# 	yield request

	def closed(self, reason):
		pass
		
	def isUnique(self, url):
		for link in self.visited_urls:
			if link == url:
				return False
		return True

