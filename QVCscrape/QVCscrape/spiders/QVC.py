# -*- coding: utf-8 -*-
import scrapy

from QVCscrape.items import QVCItem
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.response import open_in_browser

class QVCSpider(scrapy.Spider):
	failed_count = 0
	visited_urls=[]
	name = "QVC"
	allowed_domains = ["qvc.com"]
	start_urls = ["http://www.qvc.com/webapp/wcs/stores/servlet/ProgramGuideWeeklyView?storeId=10251&TimeZoneSelect=EST&weekRange=0&channelCode=QVC"]


	def parse(self, response):
		for sel in response.xpath('//tr[@class="trHour"]'):
			startTime = sel.xpath('.//span[@class="dtstart"]/text()').extract()[0]
			endtime = sel.xpath('.//span[@class="dtend"]/text()').extract()[0]
			for link in sel.xpath('.//div[@class="divSeeItems"]/a/@href'):
				link = link.extract()
				url = response.urljoin(link)
				if (self.isUnique(url)):
					self.visited_urls.append(url)
					request = scrapy.Request(url, self.day_page)
					yield request

		#old stuff
		# for sel in response.xpath('//div[@class="divSeeItems"]'):
			# link = sel.xpath('a/@href').extract()
			# url = response.urljoin(link[0])
			# if (self.isUnique(url)):
			# 	self.visited_urls.append(url)
			# 	request = scrapy.Request(url, self.day_page)
			# 	yield request


		# for sel in response.xpath('//@href'):
		# 	item = DmozItem()
		# 	item['title'] = sel.xpath('a/text()').extract()
		# 	item['link']=link = sel.xpath('a/@href').extract()
		# 	item['desc'] = sel.xpath('text()').extract()
		# 	print item['link']

	#follow day page links
	def day_page(self,response):
		daySel = response.xpath('//select[@id="selDate"]/option[@selected]')
		# daySel = response.xpath('//div[@class="divNavItemsRecentlyOnAir"]')
		if len(daySel)==0:
			self.failed_count=self.failed_count +1
			request = scrapy.Request(response.url, self.day_page)
			yield request
			# print "bork:"
			# print response.url
			# open_in_browser(response)
		day = daySel.xpath('text()').extract()
		#save day and send as meta response stuff
		if len(day)>0:
			day = day[0]

		for sel in response.xpath('//span[@class="fn description"]/a[@class="prodDetailLink url"]'):
			link = sel.xpath('@href').extract()
			url = response.urljoin(link[0])
			if (self.isUnique(url)):
				self.visited_urls.append(url)
				# request.meta['day'] = day
				# request = scrapy.Request(url, self.product_page)
				# yield request



		# for sel in links:
		# 	request = scrapy.Request(node['link'], self.follow_the_trail)
		# 	yield request
	def product_page(self, response):
		response.xpath('//div[@class="itemNo"]')




	def closed(self, reason):
		print self.failed_count
		pass
		
	def isUnique(self, url):
		for link in self.visited_urls:
			if link == url:
				return False
		return True

