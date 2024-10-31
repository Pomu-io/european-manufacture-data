import scrapy 
from scrapy_splash import SplashRequest
from europeanManufacture.items import ProductPageItem
import datetime
import time
import psycopg2
import json

class ProductLinksSpider(scrapy.Spider): 

  name="productLinksSpider"

  custom_settings = {
        'ITEM_PIPELINES': {
            'europeanManufacture.pipelines.ProductImagePipeline': 1,
        },
    }

  db_params = {
        "dbname": "europe_manufactures",
        "user": "postgres",
        "password": "qiming1021",
        "host": "localhost",
    }

  def start_requests(self): 
    print(f"time now begin: {datetime.datetime.now()}")

    # yield SplashRequest(url="https://www.europages.co.uk/ATAK-TEXTILE/00000005402778-734094001.html")

    try: 
      connection = psycopg2.connect(**self.db_params)
      cursor = connection.cursor()
      cursor.execute("ROLLBACK")
      
      # Fetch all rows from the specified table
      table_name = self.settings.get('PRODUCT_LINKS_READ_FROM_TABLE_NAME')
      cursor.execute(f"SELECT manufacture_name, europe_page_url, product_page_total FROM {table_name} WHERE product_amount != -1 LIMIT 1")
      rows = cursor.fetchall()
      
      # Loop through each row and yield a request
      for i, (manufacture_name, url, product_page_total) in enumerate(rows):
          print(f"Processing {i}th manufacture {manufacture_name} URL: {url} having {product_page_total} pages\n")
          if product_page_total != -1: 
            for cur_page in range(1, product_page_total): 
              print(f"On page {cur_page}")
              cur_page_url = url + f"?/page={cur_page}"
              print(f"cur_page_url is {cur_page_url}")

              yield SplashRequest(
              url=cur_page_url,
              callback=self.parse,
              meta={'manufacture_number': i, 'url': cur_page_url, 'manufacture_name': manufacture_name, 
              'product_page_total': product_page_total, 'cur_page': cur_page}, 
            )
          else: 
            print(f"1 page in manufacture {manufacture_name} with url {url}\n")
            yield SplashRequest(
                url=url,
                callback=self.parse,
                meta={'manufacture_number': i, 'url': url, 'manufacture_name': manufacture_name, 'product_page_total': product_page_total, 'cur_page': -1}, 
                # args={'lua_source': self.click_script(), 'wait': 1}
            )
    except Exception as e: 
      print(f"database connection error {e}")
      self.logger.error(f"Database error: {e}")
    finally: 
      self.close_connection(connection, cursor)
    
  def close_connection(self, connection, cursor):
      # Closes the database connection and cursor
      if cursor:
          cursor.close()
      if connection:
          connection.close()
  
  def parse(self, response): 

    cur_page = response.meta.get('cur_page', -1)

    manufacture_name = response.meta.get('manufacture_name', 'default_name')
    europe_page_url = response.meta.get('url', -1)
    product_page_total = response.meta.get('product_page_total', -1)
    print(f"\nReading manufacture {manufacture_name} with url {europe_page_url} page {cur_page}\n")
    self.log(f"\nProcessing manufacture {manufacture_name} with url {europe_page_url} page {cur_page}\n")
    product_links = response.xpath("//a[@data-test='product-image']/@href").getall()

    product_page_item = ProductPageItem(
      manufacture_name = manufacture_name, 
      europe_page_url = europe_page_url,  
      product_links = product_links, 
    )
    
    print(f"In spider parse response, manufacture is {product_page_item['manufacture_name']}")
    
    # what should be sent request to, or just get them all in all pages, then visit them one by one
    print(f"productPageItem in spider parse function is: {product_page_item}")

    yield product_page_item
  
