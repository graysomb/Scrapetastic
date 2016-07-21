# Scrapetastic
website scraper that currently uses scrapy to navigate through html code and requests to obtain useful information. selenium is used for clicking or injecting javascript. currently they can only interact by selenium passing scrapy href links.

### to install (assuming you have python 2.7)
```
sudo apt-get install python-dev python-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev
sudo pip install scrapy
sudo pip install selenium
sudo apt-get install xvfb
sudo pip install pyvirtualdisplay
sudo apt-get install xserver-xephyr
```
add the Scraptastic folder to path, this is so selenium can find the "wires" binary and "chromedriver" binary
```
export PATH=~/Code/Scrapetastic:$PATH
```
###to run 
navigate to QVCscrape and do
```
scrapy crawl QVC
```
in general 
```
scrapy crawl SpiderName
```
to test out xpath selectors on a website
```
scrapy shell "someHtmlLink.com"
```
then 
```
>>> response.xpath('some selectors')
```
### some docs:
http://doc.scrapy.org/en/latest/

http://selenium-python.readthedocs.io/getting-started.html

