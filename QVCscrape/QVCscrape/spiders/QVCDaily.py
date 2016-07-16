# -*- coding: utf-8 -*-
import scrapy

from QVCscrape.items import QVCDailyItem
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.response import open_in_browser
import time

class QVCDailySpider(scrapy.Spider):
	visited_urls=[]
	itemCount = 0
	name = "QVCDaily"
	day_count=0
	day_visited=0
	allowed_domains = ["qvc.com"]
	start_urls = ["http://www.qvc.com/webapp/wcs/stores/servlet/ProgramGuideDailyView?storeId=10251&TimeZoneSelect=EST&Navigate=20160713&channelCode=QVC"]


	def parse(self, response):
		sels = response.xpath('//div[@class="divProgramInformationWrapper"]//div[@class="divSeeItems"]/a/@href').extract()
		sels2 = response.xpath('//div[@class="divProgramDetailsInformation"]')
		if len(sels)!=len(sels2):
			print "Warning: number of shows and links don't match"
		for i in range(0,len(sels)-1):
			request = scrapy.Request(response.urljoin(sels[i]), self.parse_show)
			request.meta['show'] = sels2[i].xpath('.//h3/text()').extract()[0]
			request.meta['day'] = sels2[i].xpath('.//div/text()').extract()[0]
			request.meta['time'] = sels2[i].xpath('.//div/span/text()').extract()[0]+" - "+sels2[i].xpath('.//div/span/text()').extract()[1]
			request.meta['show_description'] = sels2[i].xpath('.//span[@class="summary"]').extract()[0]
			yield request

	#follow day page links
	def parse_show(self,response):
		if len(response.xpath('//span[@class="fn description"]/a[@class="prodDetailLink url"]'))==0:
			print "Warning: no items"
		for sel in response.xpath('//span[@class="fn description"]/a[@class="prodDetailLink url"]'):
			link = sel.xpath('@href').extract()
			url = response.urljoin(link[0])
			if (self.isUnique(url)):
				self.visited_urls.append(url)
				request = scrapy.Request(url, self.parse_product)
				request.meta['show'] = response.meta['show']
				request.meta['day'] = response.meta['day']
				request.meta['time'] = response.meta['time']
				request.meta['show_description'] = response.meta['show_description'] 
				yield request



		# for sel in links:
		# 	request = scrapy.Request(node['link'], self.follow_the_trail)
		# 	yield request
	def parse_product(self, response):
		item = QVCDailyItem()
		item['url'] = response.url
		item['show'] = response.meta['show']
		item['show_description'] = response.meta['show_description']
		item['day'] = response.meta['day']
		item['time'] = response.meta['time']

		itemNumber=response.xpath('//div[@class="itemNo"]/text()').extract()
		if len(itemNumber)>0:
			item['number'] = itemNumber[0]
		itemName = response.xpath('//div[@class="pdShortDesc"]/div/h1/text()').extract()
		if len(itemName)>0:
			item['name'] = itemName[0]
		itemBefPrice = response.xpath('//div[@class="qvcPrice"]/span/text()').extract()
		if len(itemBefPrice)>0:
			item['beforePrice'] = itemBefPrice[0]
		itemPrice =response.xpath('//div[@class="featuredPrice"]/span/text()').extract()
		if len(itemPrice)>0:
			item['Price']= itemPrice[0]
		itemDescription = response.xpath('//div[@class="accordionText"]/text()').extract()
		if len(itemDescription)>0:
			item['description'] = itemDescription[0]

		self.itemCount = self.itemCount+1
		yield item







	def closed(self, reason):
		print self.itemCount
		
	def isUnique(self, url):
		for link in self.visited_urls:
			if link == url:
				return False
		return True

