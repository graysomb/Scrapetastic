# -*- coding: utf-8 -*-
import scrapy

from QVCscrape.items import QVCDailyItem
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.response import open_in_browser
import time

class HSNSpider(scrapy.Spider):
	visited_urls=[]
	itemCount = 0
	name = "HSN"
	day_count=0
	day_visited=0
	allowed_domains = ["hsn.com"]
	start_urls = ["http://www.hsn.com/watch/program-guide?disp=1"]


	def parse(self, response):
		sel = response.xpath('//div[@class="show-detail-container"]')
		for link in sel:
			url = response.xpath('/div[@class="shop-more-items"]/@href').extract()[0]
			request = scrapy.Request(response.urljoin(url), self.parse_show)
			request.meta['show'] = response.xpath('/div[@class="show-detail-header"]/span/text()').extract()[0]
			timeInfo = response.xpanth('.//div[@class="date-card"]/div/text()').extract()
			request.meta['day']  = timeInfo[0] + " "+timeInfo[1]
			request.meta['time'] = timeInfo[3]
			request.meta['show_description'] = response.xpath('/div[@class="show-detail-header"]/span/text()').extract()[1]
			yield request

	#follow day page links
	def parse_show(self,response):
		if len(response.xpath('//div[@class="info"]/a/@href'))==0:
			print "Warning: no items"
		for sel in response.xpath('//div[@class="info"]/a/@href'):
			link = sel.extract()
			url = response.urljoin(link[0])
			if (self.isUnique(url)):
				self.visited_urls.append(url)
				request = scrapy.Request(url, self.parse_product)
				request.meta['show'] = response.meta['show']
				request.meta['day'] = response.meta['day']
				request.meta['time'] = response.meta['time']
				request.meta['show_description'] = response.meta['show_description'] 
				yield request


	def parse_product(self, response):
		item = QVCDailyItem()
		item['url'] = response.url
		item['show'] = response.meta['show']
		item['show_description'] = response.meta['show_description']
		item['day'] = response.meta['day']
		item['time'] = response.meta['time']

		itemNumber=response.xpath('//div[@class="item-number"]/text()').extract()
		if len(itemNumber)>0:
			item['number'] = itemNumber[0]
		itemName = response.xpath('//span[@id="product-name"]/text()').extract()
		if len(itemName)>0:
			item['name'] = itemName[0]
		itemBefPrice = response.xpath('//div[@class="product-retail-price space-top "]/text()').extract()
		if len(itemBefPrice)>0:
			item['beforePrice'] = itemBefPrice[0]
		itemPrice =response.xpath('//span[@class="product-price"]/text()').extract()
		if len(itemPrice)>0:
			item['Price']= itemPrice[0]
		itemDescription = response.xpath('//div[@class="content copy"]/div/text()').extract()
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

