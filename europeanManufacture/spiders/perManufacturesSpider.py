import scrapy 
from scrapy_splash import SplashRequest
from europeanManufacture.items import PerManufactureItem
import datetime
import time
import psycopg2
import json

class PerManufactureSpider(scrapy.Spider): 

  name="perManufacture"

  db_params = {
        "dbname": "europe_manufactures",
        "user": "postgres",
        "password": "qiming1021",
        "host": "localhost",
    }

  def start_requests(self): 
    print(f"time now begin: {datetime.datetime.now()}")

    try: 
      connection = psycopg2.connect(**self.db_params)
      cursor = connection.cursor()
      cursor.execute("ROLLBACK")
      
      # Fetch all rows from the specified table
      table_name = self.settings.get('PER_MANUFACTURE_READ_FROM_TABLE_NAME', 'EXCEpTION_NAME_name_url')
      cursor.execute(f"SELECT manufacture_name, url FROM {table_name}")
      rows = cursor.fetchall()
      
      # Loop through each row and yield a request
      for i, (manufacture_name, url) in enumerate(rows):
          print(f"Processing {i}th manufacture {manufacture_name} URL: {url}\n")
          yield SplashRequest(
              url=url,
              callback=self.parse,
              meta={'manufacture-number': i, 'url': url, 'manufacture_name': manufacture_name}, 
              # args={'lua_source': self.click_script(), 'wait': 1}
          )
    except Exception as e: 
      print(f"database connection error {e}")
      self.logger.error(f"Database error: {e}")
    finally: 
      self.close_connection(connection, cursor)

  def parse(self, response): 

    name = response.xpath("//a/h1/text()").get(-1)
    europe_page_url = response.meta['url']
    company_website = response.xpath("//a[contains(@class, 'website-button')]/@href").get(default=-1)
    
    delivery = response.xpath('.//div[@data-test="distribution-area"]//text()').getall()[1] if response.xpath('.//div[@data-test="distribution-area"]//text()') else -1
    location = response.xpath("//div[@class='font-copy-400 text-navy-70 ep:text-darkgreen-70']/div/text()").get(default=-1)
    country = response.xpath("//div[@class='font-copy-400 text-navy-70 ep:text-darkgreen-70']//span/text()").get(default=-1)
  
    founded_time = response.xpath("//div[@data-test='founding-year']//strong/text()").get(default=-1)
    employee_number = response.xpath("//div[@data-test='employee-count']//strong/text()").get(default=-1)
    supplier_type = response.xpath("//div[@data-test='supplier-types']//span/text()").get(default=-1)
    about_us = response.xpath('.//div[@data-test="description"]//text()').getall()[1] if response.xpath('.//div[@data-test="description"]//text()') else -1
    product_amount = int(response.xpath("//h2[@class='title no-margin font-display-500 col-span-1 md:col-span-2 order-2']/text()").get()[:-20]) if response.xpath("//h2[@class='title no-margin font-display-500 col-span-1 md:col-span-2 order-2']/text()") else -1
    product_page_total = response.xpath("//a[@data-test='pagination-number']/text()").getall()[-1] if response.xpath("//a[@data-test='pagination-number']/text()") else -1
    key_words = ', '.join ([item.strip() for item in response.xpath("//div[contains(@class, 'flex flex-wrap gap-1')]//a[@class='item']/text()").getall()])
    if response.css('script#\\__NUXT_DATA__::text'):
      script_content = response.css('script#\\__NUXT_DATA__::text').get()
      data = json.loads(script_content)
      check_list = [i for i in data if isinstance(i, str) and "+" in i]
      phone_number = check_list[0] if check_list else -1
    else: 
      phone_number = -1
    
    response.xpath('//div[@class="label inline-flex items-center rounded-sm max-w-full gap-[6px] whitespace-nowrap px-0.5 md:px-1 py-[2px]"]/span/text()').getall()
    
    VAT_number = 1 if response.xpath("//div[@data-test='vat-number-button']") else -1

    item_manufacture = PerManufactureItem (
      name = name, 
      europe_page_url = europe_page_url, 
      company_website = company_website, 
      location = location, 
      country = country, 
      phone_number = phone_number, 

      VAT_number = VAT_number, 
      # average_response_time = scrapy.Field()
      # average_response_rate = scrapy.Field()
      delivery = delivery, 
      founded_time = founded_time, 
      employee_number = employee_number, 
      supplier_type = supplier_type, 
      about_us = about_us, 
      product_amount = product_amount, 
      product_page_total = product_page_total, 
      key_words = key_words, 
    )

    print(f"\nitem obtained from {name} and {europe_page_url} is\n {item_manufacture}\n")

    yield item_manufacture
  

