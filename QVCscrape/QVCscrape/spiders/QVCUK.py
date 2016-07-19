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
	name = "QVCUK"
	day_count=0
	day_visited=0
	allowed_domains = ["qvcuk.com"]
	start_urls = ["http://www.qvcuk.com/ItemsRecentlyOnAirView?storeId=10252&catalogId=10152&langId=-2"]

	def __init__(self):
		self.display = Display(visible=1, size=(1024, 768))
		self.display.start()
		firefox_capabilities = DesiredCapabilities.FIREFOX
		firefox_capabilities['marionette'] = True
		self.driver = webdriver.Firefox(capabilities=firefox_capabilities)


	def parse(self, response):
		self.driver.get(response.url)
		numOpts = len(response.xpath('//select[@id="selDate"]/option'))
		for i in range(1, numOpts):
			self.driver.execute_script('document.getElementById("selDate").options.selectedIndex = '+str(i)+'; document.getElementById("selDate").onchange();')
			time.sleep(2)
			links = self.driver.find_elements_by_xpath('//ul[@class="noCheckBox"]/li/a')
			j=0
			for link in links:
				print link.get_attribute("href")
				request = scrapy.Request(link.get_attribute("href"), self.parse_shows, dont_filter=True)
				request.meta['show'] = link.text
				request.meta['time'] = self.driver.find_elements_by_xpath('//li/span[@class="showTime"]')[j].text
				request.meta['day'] = self.driver.find_element_by_id('firstItemsRecentlyOnAirH').text
				j = j+1
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
		item['Price'] = response.xpath('//div[@class="qvcPrice"]/span/text()').extract()[0]
		item['description'] = response.xpath('//div[@class="accordionText"]/text()').extract()[0]
		yield item

	def closed(self, reason):
		print self.itemCount
		self.driver.close()
		self.display.stop()

