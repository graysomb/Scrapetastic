# Scrapetastic
website scraper that currently uses scrapy to navigate through html code and requests to obtain useful information. selenium is used for clicking or injecting javascript. currently they can only interact by selenium passing scrapy href links.

### to install 
```
sudo apt-get install python-dev python-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev
sudo pip install scrapy
sudo pip install selenium
sudo apt-get install xvfb
sudo pip install pyvirtualdisplay
sudo apt-get install xserver-xephyr
```
add the Scraptastic folder to path, unless selenium now supports firefox 47 drivers

###to run navigate to QVCscrape
```
scrapy crawl QVC
```
in general 
```
scrapy crawl SpiderName
```
### some docs:
http://doc.scrapy.org/en/latest/

http://selenium-python.readthedocs.io/getting-started.html

