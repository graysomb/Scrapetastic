# -*- coding: utf-8 -*-
import scrapy

from QVCscrape.items import QVCUKItem
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.response import open_in_browser
from selenium import webdriver
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
		self.display = Display(visible=0, size=(1024, 768))
		self.display.start()
		firefox_capabilities = DesiredCapabilities.FIREFOX
		firefox_capabilities['marionette'] = True
		self.driver = webdriver.Firefox(capabilities=firefox_capabilities)


	def parse(self, response):
		self.driver.get(response.url)
		print len(self.driver.find_element_by_xpath('//select[@id="selDate"]'))
			# while True:
			# 	try:
			# 		dropdown = self.driver.find_element_by_xpath('//select[@id="selDate"]')[0]
			# 		url = response.url
			# 		yield Request(url, self.parse2)
			# 		next.click()
			# 	except:
			# 		break

	#follow day page links
	def parse2(self,response):
		open_in_browser(response)


	def closed(self, reason):
		print self.itemCount
		self.display.stop()
		self.driver.close()

	def isUnique(self, url):
		for link in self.visited_urls:
			if link == url:
				return False
		return True

