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
            'europeanManufacture.pipelines.ProductLinksPipeline': 1,
        },
    }

  db_params = {
        "dbname": "europe_manufactures",
        "user": "postgres",
        "password": "qiming1021",
        "host": "localhost",
    }
  
  def __init__(self): 
    super().__init__()
    self.manufacture_data = {}

  def start_requests(self): 
    print(f"time now begin: {datetime.datetime.now()}")

    try: 
      connection = psycopg2.connect(**self.db_params)
      cursor = connection.cursor()
      cursor.execute("ROLLBACK")
      
      # Fetch all rows from the specified table
      table_name = self.settings.get('PRODUCT_LINKS_READ_FROM_TABLE_NAME')
      cursor.execute(f"SELECT manufacture_name, europe_page_url, product_page_total FROM {table_name} WHERE product_amount != -1")
      rows = cursor.fetchall()
      
      # Loop through each row and yield a request
      for i, (manufacture_name, url, product_page_total) in enumerate(rows):
        self.manufacture_data[manufacture_name] = []
        print(f"Processing {i}th manufacture {manufacture_name} URL: {url} having {product_page_total} pages\n")
        if product_page_total != -1: 
          for cur_page in range(1, product_page_total+1): 
            print(f"On page {cur_page}")
            cur_page_url = url + f"?page={cur_page}"
            print(f"cur_page_url is {cur_page_url}")

            yield SplashRequest(
            url=cur_page_url,
            callback=self.parse,
            meta={'manufacture_number': i, 'europage_url': url,'cur_page_url': cur_page_url, 'manufacture_name': manufacture_name, 
            'product_page_total': product_page_total, 'cur_page': cur_page}, 
            # dont_filter=True
          )
        else: 
          print(f"1 page in manufacture {manufacture_name} with url {url}\n")
          yield SplashRequest(
              url=url,
              callback=self.parse,
              meta={'manufacture_number': i, 'url': url, 'manufacture_name': manufacture_name, 'product_page_total': product_page_total, 'cur_page': -1}, 
          )
    except Exception as e: 
      print(f"database connection error {e}")
      self.logger.error(f"Database error: {e}")
    finally: 
      self.close_connection(connection, cursor)
  
  def parse(self, response): 

    print("parsing...")

    cur_page = response.meta.get('cur_page', -1)

    manufacture_name = response.meta.get('manufacture_name', 'default_name')
    europe_page_url = response.meta.get('europage_url', -1)
    product_page_total = response.meta.get('product_page_total', -1)
    print(f"\nReading manufacture {manufacture_name} with url {europe_page_url} page {cur_page}\n")
    self.log(f"\nProcessing manufacture {manufacture_name} with url {europe_page_url} page {cur_page}\n")
    
    product_links = response.xpath("//a[@data-test='product-image']/@href").getall()
    if manufacture_name in self.manufacture_data: 
      print(f"manufacture_name is {manufacture_name}")
      # print(f"\nCurrent manufacture_data[manufacture_name] is {self.manufacture_data[manufacture_name]}\n")
      self.manufacture_data[manufacture_name].extend(product_links)
      # print(f"Is extended? length or product_links {len(product_links)} VS length of manufacture_data[manufacture_name] {len(self.manufacture_data[manufacture_name])}")
    
    # Only last page yielding item and write to pipeline
    if cur_page == product_page_total or cur_page == -1: 

      print("reaching the last page")
      print(f"manufacture name is {manufacture_name}")
      yield ProductPageItem(
        manufacture_name = manufacture_name, 
        europe_page_url = europe_page_url,  
        product_links = self.manufacture_data[manufacture_name], 
      )
  
  def close_connection(self, connection, cursor):
      # Closes the database connection and cursor
      if cursor:
          cursor.close()
      if connection:
          connection.close()
