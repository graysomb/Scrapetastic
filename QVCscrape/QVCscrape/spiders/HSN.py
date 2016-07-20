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
	name = "HSN"
	day_count=0
	day_visited=0
	allowed_domains = ["hsn.com"]
	start_urls = ["http://www.hsn.com/watch/program-guide"]

	def __init__(self):
		self.display = Display(visible=1, size=(1024, 768))
		self.display.start()
		# firefox_capabilities = DesiredCapabilities.FIREFOX
		# firefox_capabilities['marionette'] = True
		# self.driver = webdriver.Firefox(capabilities=firefox_capabilities)
		self.driver = webdriver.Chrome()

	def parse(self,response):
		self.driver.get(response.url)
		# time.sleep(5)
		target = self.driver.find_element_by_xpath('//select[@id="change-date"]')
		options = self.driver.find_elements_by_xpath('//select[@id="change-date"]/option')
		target.click()
		time.sleep(1)
		options[0].click()
		# ActionChains(self.driver).click_and_hold(target).click(options[0]).perform()
		# options[0].send_keys(Keys.RETURN)
		time.sleep(5)

	def parse2(self, response):
		selurl = response.xpath('//div[@class="cell shop"]')
		selshows = response.xpath('//div[@class="cell show"]/span/text()')
		seltimes = response.xpath('//div[@class="cell time "]/div/text()')
		if len(selurl) != len(selshows) or len(selshows) != len(seltimes) or len(selurl) != len(seltimes):
			print "Warning: mismatched links and data"
		for i in range(0,len(selurl)-1):
			url = selurl[i].xpath('./a/@href').extract()[0]
			print url
			request = scrapy.Request(response.urljoin(url), self.parse_show)
			request.meta['show'] = selshows[i].extract()
			request.meta['day']  = response.xpath('//select[@class="date"]/option[@selected]/text()').extract()[0]
			request.meta['time'] = seltimes.extract()[0]
			yield request

	#follow day page links
	def parse_show(self,response):
		if len(response.xpath('//div[@class="info "]/h3/a/@href'))==0:
			print "Warning: no items"
		for sel in response.xpath('//div[@class="info "]/h3/a/@href'):
			link = sel.extract()
			url = response.urljoin(link)
			request = scrapy.Request(url, self.parse_product)
			request.meta['show'] = response.meta['show']
			request.meta['day'] = response.meta['day']
			request.meta['time'] = response.meta['time']
			yield request


	def parse_product(self, response):
		item = QVCDailyItem()
		item['url'] = response.url
		item['show'] = response.meta['show']
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
		itemDescription =response.xpath('//div[@class="content copy"]/div/text()').extract()
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

