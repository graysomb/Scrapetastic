# -*- coding: utf-8 -*-
import scrapy

from QVCscrape.items import QVCDailyItem
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.response import open_in_browser
import time

class QVCDailySpider(scrapy.Spider):
	visited_urls=[]
	itemCount = 0
	name = "JTV"
	day_count=0
	day_visited=0
	allowed_domains = ["jtv.com"]
	start_urls = ["http://www.jtv.com/ProgramGuideArchive"]


	def parse(self, response):
		sels = response.xpath('//table[@class="an_prod"]')
		print len(sels)
		for sel in sels:
			day = sel.xpath('./tr/td/a/text()').extract()[0]
			url = sel.xpath('./tr/td/a/@href').extract()[0]
			request = scrapy.Request(response.urljoin(url), self.parse_show)
			request.meta['day'] = day
			yield request


	#follow day page links
	def parse_show(self,response):
		nextPage = response.xpath('//a[@class="right_arrow"]/@href')
		if len(nextPage)>0:
			print len(nextPage)
			request = scrapy.Request(response.urljoin(nextPage.extract()[0]), self.parse_show)
			request.meta['day'] = response.meta['day']
			yield request
		sels = response.xpath('//div[@class="product producttile"]/div[@class="name"]/a/@href')
		for sel in sels:
			url = sel.extract()
			request = scrapy.Request(response.urljoin(url), self.parse_product)
			request.meta['day'] = response.meta['day']
			yield request



		# for sel in links:
		# 	request = scrapy.Request(node['link'], self.follow_the_trail)
		# 	yield request
	def parse_product(self, response):
		item = QVCDailyItem()
		item['url'] = response.url
		item['day'] = response.meta['day']

		itemNumber=response.xpath('///div[@id="addtocart"]/div[@id="sku-row"]/span[@class="sku"]/text()').extract()
		if len(itemNumber)>0:
			item['number'] = itemNumber[0]
		itemName = response.xpath('//div[@id="media-addtocart-row"]/div[@id="addtocart"]/div[@id="title-row"]/h1/text()').extract()
		if len(itemName)>0:
			item['name'] = itemName[0]
		itemBefPrice = response.xpath('//div[@id="product-price-row"]/span[@class="product-retail-price"]/span[@id="retail-price"]/text()').extract()
		if len(itemBefPrice)>0:
			item['beforePrice'] = itemBefPrice[0]
		itemPrice =response.xpath('//span[@class="product-sale-price"]/div[@class="product-price"]/text()').extract()
		if len(itemPrice)>0:
			item['Price']= itemPrice[0]
		itemDescription = response.xpath('//div[@id="product-desj-tab-row"]/div[@class="col-xs-12 row"]/div[@id="description"]/div[2]/text()').extract()
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

