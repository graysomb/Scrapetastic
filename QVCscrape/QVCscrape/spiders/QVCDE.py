# -*- coding: utf-8 -*-
import scrapy
import time

from QVCscrape.items import QVCUKItem
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.response import open_in_browser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from pyvirtualdisplay import Display
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class QVCUKSpider(scrapy.Spider):
	visited_urls=[]
	itemCount = 0
	name = "QVCDE"
	day_count=0
	day_visited=0
	allowed_domains = ["qvc.de"]
	start_urls = ["http://www.qvc.de/ItemsRecentlyOnAirView?langId=-3&storeId=10253&catalogId=10153&sc=TVRB"]

	def __init__(self):
		self.display = Display(visible=1, size=(1024, 768))
		self.display.start()
		# firefox_capabilities = DesiredCapabilities.FIREFOX
		# firefox_capabilities['marionette'] = True
		# self.driver = webdriver.Firefox(capabilities=firefox_capabilities)
		self.driver = webdriver.Chrome()

	def parse(self, response):
		sels = response.xpath('//div[@id="divNavSpotlight"]/ul/li/a')
		for sel in sels:
			url = sel.xpath('./@href').extract()[0]
			day = sel.xpath('./text()').extract[0]
			request = scrapy.Request(response.urljoin(url), self.parse_days)
			request.meta['day'] = day
			yield request

	def parse_days(self, response):
		sels = response.xpath('//ul[@class="noCheckBox"]')
		for sel in sels:
			url = sel.xpath('./a/@href').extract()[0]
			time = sel.xpath('./span/text()').extract()[0]
			show = sel.xpath('./a/text()').extract()[0]
			request = scrapy.Request(response.urljoin(url), self.parse_shows)
			request.meta['time'] = time
			request.meta['show'] = show
			yield request

	#follow day page links
	def parse_shows(self,response):
		for sel in response.xpath('//a[@class="prodDetailLink"]/@href'):
			request = scrapy.Request(sel.extract(), self.parse_products)
			request.meta['show'] = response.meta['show']
			request.meta['time'] = response.meta['time']
			request.meta['day'] = response.meta['day']
			yield request

	def parse_products(self, response):
		item = QVCUKItem()
		item['url'] = response.url
		item['time'] = response.meta['time']
		item['show'] = response.meta['show']
		item['day'] = response.meta['day']
		item['number'] = response.xpath('//div[@class="itemNo"]/text()').extract()[0]
		item['name'] = response.xpath('//div[@class="pdShortDesc"]/div/h1/text()').extract()[0]
		item['Price'] = response.xpath('//div[@class="featuredPrice"]/span/text()').extract()[0]
		item['description'] = response.xpath('//div[@class="tab-content-ipim"]/text()').extract()[0]
		yield item

	def closed(self, reason):
		print self.itemCount
		self.driver.close()
		self.display.stop()

