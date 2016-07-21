# -*- coding: utf-8 -*-
import scrapy

from QVCscrape.items import QVCDailyItem
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.response import open_in_browser
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
#this is currently daily
class HSNSpider(scrapy.Spider):
	visited_urls=[]
	itemCount = 0
	name = "EVINE"
	day_count=0
	day_visited=0
	allowed_domains = ["evine.com"]
	start_urls = ["http://www.evine.com/OnAir/ProgramGuide/18424765#content"]

	def __init__(self):
		self.display = Display(visible=1, size=(1024, 768))
		self.display.start()
		# firefox_capabilities = DesiredCapabilities.FIREFOX
		# firefox_capabilities['marionette'] = True
		# self.driver = webdriver.Firefox(capabilities=firefox_capabilities)
		self.driver = webdriver.Chrome()

	def parse(self,response):
		self.driver.get(response.url)
		self.driver.find_element_by_xpath('//div[@class="ui-state-default icon-div jQButtonNoWidth"]').click()
		time.sleep(1)
		targets = self.driver.find_elements_by_xpath('//a[@class="actionLink "]')
		scrollNum = len(self.driver.find_elements_by_xpath('//tr[@class="odd"]')[0].find_elements_by_xpath('.//td'))
		count = 0
		for target in targets:
			target.click()
			time.sleep(1)
			show = target.text
			date = self.driver.find_element_by_xpath('//div[@class="show-date"]').text
			scrollbar = self.driver.find_element_by_xpath('//div[@class="touchcarousel-wrapper auto-cursor"]')
			action = ActionChains(self.driver)
			action.move_to_element(scrollbar)
			action.click()
			for i in range(1,4):
				action.send_keys(Keys.ARROW_RIGHT)
			action.perform()
			time.sleep(1)
			count = count + 1
			links = self.driver.find_elements_by_xpath('//a[@class="product-description"]')
			for link in links:
				url = link.get_attribute("href")
				request = scrapy.Request(response.urljoin(url), self.parse_product)
				request.meta['day'] = date
				request.meta['show'] = show
				print len(targets)
				yield request


	def parse_product(self, response):
		item = QVCDailyItem()
		item['url'] = response.url
		item['show'] = response.meta['show']
		item['day'] = response.meta['day']

		itemNumber=response.xpath('//div[@class="product-detail-title"]/span[2]/text()').extract()
		if len(itemNumber)>0:
			item['number'] = itemNumber[0]
		itemName = response.xpath('//div[@class="product-detail-title"]/span[1]/text()').extract()
		if len(itemName)>0:
			item['name'] = itemName[0]
		itemBefPrice = response.xpath('//span[@class="priceBlockRetailPrice"]/text()').extract()
		if len(itemBefPrice)>0:
			item['beforePrice'] = itemBefPrice[0]
		itemPrice =response.xpath('//span[@id="listedPrice"]/text()').extract()
		if len(itemPrice)>0:
			item['Price']= itemPrice[0]
		itemDescription =response.xpath('//div[@id="long-description"]/text()').extract()
		if len(itemDescription)>0:
			item['description'] = itemDescription[0]

		self.itemCount = self.itemCount+1
		yield item


	def closed(self, reason):
		print self.itemCount
		self.driver.close()
		self.display.stop()
		
	def isUnique(self, url):
		for link in self.visited_urls:
			if link == url:
				return False
		return True

