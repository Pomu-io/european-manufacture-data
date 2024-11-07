import scrapy 
from scrapy_splash import SplashRequest
from europeanManufacture.items import ProductDetailItem, ProductImageItem
import datetime
import time
import psycopg2
import json

class ProductLinksSpider(scrapy.Spider): 

  name="productDetailSpider"

  custom_settings = {
        'ITEM_PIPELINES': {
            'europeanManufacture.pipelines.ProductDetailPipeline': 100,
            'europeanManufacture.pipelines.ProductImagePipeline': 200,
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
      table_name = self.settings.get('PRODUCT_DETAILS_READ_FROM_TABLE_NAME')
      cursor.execute(f"SELECT manufacture_name, product_links FROM {table_name} ORDER BY RANDOM() LIMIT 3")
      # cursor.execute(f"SELECT manufacture_name, product_links FROM {table_name} LIMIT 2")
      rows = cursor.fetchall()

      base_url="https://www.europages.co.uk"
      # Loop through each row and yield a request
      for i, (manufacture_name , product_links) in enumerate(rows):
        print("--——------------------------------------------------")
        print(f"Getting {i+1}th manufacture {manufacture_name}\n")
        self.manufacture_data[manufacture_name] = []
        # product_links is a text string with "," separate every item; get item to lists
        product_links = product_links.split(", ")
        # add base url to product_links
        full_urls = [base_url+img_url for img_url in product_links]

        # Visit every product detail page. 
        for j, per_url in enumerate(full_urls): 
          print(f"\nGetting manufacture {manufacture_name} product {per_url}\n")
          if j+1 == len(full_urls): 
            print(f"Last product NO.{j+1} for manufacture {manufacture_name}")
            yield SplashRequest(
            url=per_url, 
            callback=self.parse,
            meta={'manufacture_number': i, 'product_number': j, 'manufacture_name': manufacture_name, 'last_one': True}, 
          ) 
          else: 
            yield SplashRequest(
            url=per_url, 
            callback=self.parse,
            meta={'manufacture_number': i, 'product_number': j, 'manufacture_name': manufacture_name, 'last_one': False}, 
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

    manufacture_name = response.meta.get('manufacture_name', 'default_name')
    europe_page_url = response.meta.get('url', -1)
    manufacture_number = response.meta.get('manufacture_number')+1
    product_number = response.meta.get('product_number') + 1  # it starts from 0
    last_product = response.meta.get('last_one', -1)
    product_url = response.url
    
    print(f"\nHi I am parse function. I am on No.{manufacture_number} manufacture now. Name is {manufacture_name} with product No.{product_number} \n")

    product_name = response.xpath("//h1/text()").get(default=-1)
    product_image_link = response.xpath("//a[@data-test='active-image']/img/@src").get(default=-1)
    product_description = response.xpath("//div[@class='description font-copy-400 whitespace-pre-line break-anywhere']/text()").get(default=-1)
    product_keywords = response.xpath(".//div[@class='flex flex-wrap items-center gap-1']//a/text()").getall()
    # print(f"product_keywords is {product_keywords}")

    if manufacture_name in self.manufacture_data: 
      self.manufacture_data[manufacture_name].append({
        f"product_{product_number}_name": product_name, 
        f"product_{product_number}_url": product_url, 
        f"product_{product_number}_description": product_description, 
        f"product_{product_number}_keywords": product_keywords, 
        f"product_{product_number}_image_link": product_image_link
      })

    # print("--——------------------------------------------------")
    # print(f"Length: {len(self.manufacture_data[manufacture_name])}")
    # print(f"self.manufacture_data[manufacture_name] is {self.manufacture_data[manufacture_name]}")
    # for key, value in self.manufacture_data[manufacture_name]: 
    #   print(f"{key}: {value}")
    # print("--——------------------------------------------------")

    if last_product: 
      product_name = {}
      product_image_link = {}
      product_url = {}
      product_description = {}
      product_keywords = {}
      for product in self.manufacture_data[manufacture_name]:
        for key, value in product.items(): 
          if "name" in key: 
            product_name[key] = value
          elif "description" in key: 
            product_description[key] = value
          elif "url" in key: 
            product_url[key] = value
          elif "keywords" in key: 
            product_keywords[key] = value
          elif "link" in key: 
            product_image_link[key] = value

      # Constructing image_pipeline_item 
      image_pipeline_item = {}
      for name_key, name_value in product_name.items(): 
        for link_key, link_value in product_image_link.items(): 
          # print(f"current name_key is {name_key}, link_key is {link_key}")
          if name_key[:-5] in link_key: 
            image_pipeline_item[name_value] = link_value
          # print(f"current image_pipeline_item is {image_pipeline_item}")
      
      product_detail_item = ProductDetailItem(
        manufacture_name = manufacture_name, 
        europe_page_url = europe_page_url, 
        product_name = product_name, 
        product_url = product_url, 
        product_image_link = product_image_link, 
        product_description = product_description, 
        product_keywords = product_keywords, 
      )

      yield product_detail_item

      product_image_item = ProductImageItem(
        manufacture_name = manufacture_name, 
        # store as { product_name: img_link, product_name: img_link ... }
        image_pipeline_item = image_pipeline_item, 
        image_urls = list(image_pipeline_item.values())
      )

      yield product_image_item

