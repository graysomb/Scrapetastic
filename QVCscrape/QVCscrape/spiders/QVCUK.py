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
			print "element: "
			print self.driver.find_element_by_id("firstItemsRecentlyOnAirH").text
			links = self.driver.find_elements_by_class_name("prodDetailLink")
			for link in links:
				print link.get_attribute("href")

		# url = "http://www.qvcuk.com/ItemsRecentlyOnAirView"
		# request = scrapy.Request(url, self.parse2, dont_filter=True)
		# yield request
	#follow day page links
	def parse2(self,response):
		open_in_browser(response)


	def closed(self, reason):
		print self.itemCount
		self.driver.close()
		self.display.stop()

	def isUnique(self, url):
		for link in self.visited_urls:
			if link == url:
				return False
		return True

