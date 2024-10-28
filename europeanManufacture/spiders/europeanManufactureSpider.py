import scrapy 
from scrapy_splash import SplashRequest
from europeanManufacture.items import ManufactureItem
import datetime
import time

class EuropeanManufactureSpider(scrapy.Spider): 

  name="EuropeanManufactureSpider"

  def start_requests(self): 
    print(f"time now begin: {datetime.datetime.now()}")
    for i in range(1, 79): 
      # print(f"In page {i}... \n")
      # url=f"https://www.europages.co.uk/companies/pg-{i}/apparel.html"
      # url=f"https://www.europages.co.uk/companies/pg-{i}/luxury.html"
      # url=f"https://www.europages.co.uk/companies/pg-{i}/fashion.html"
      url=f"https://www.europages.co.uk/companies/pg-{i}/shoe.html"
      self.logger.info(f"Requesting URL: {url}") 

      yield SplashRequest(url=url, callback=self.parse, meta={'page': i})

  def parse(self, response): 
    page = response.meta['page']
    manufacture_names = response.xpath(".//a[@data-test='company-name']/span/text()").getall()
    raw_urls = response.xpath(".//a[@data-test='company-name']/@href").getall()
    complete_urls = ["https://www.europages.co.uk"+raws for raws in raw_urls ]

    print(f"\nGet {len(manufacture_names)} manufactures! \n")

    for name, url in zip(manufacture_names, complete_urls): 
      item = ManufactureItem(
        name=name, 
        url=url
      )
      
      yield item
    
    print(f"\nFinished processing page {page}. Moving to the next page...\n")

