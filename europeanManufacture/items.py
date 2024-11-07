# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ManufactureItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    url = scrapy.Field()  
    
class PerManufactureItem(scrapy.Item): 
    name = scrapy.Field()
    europe_page_url = scrapy.Field()
    company_website = scrapy.Field()
    location = scrapy.Field()
    country = scrapy.Field()
    phone_number = scrapy.Field()
    VAT_number = scrapy.Field()
    average_response_time = scrapy.Field()
    average_response_rate = scrapy.Field()
    delivery = scrapy.Field()
    founded_time = scrapy.Field()
    employee_number = scrapy.Field()
    supplier_type = scrapy.Field()
    about_us = scrapy.Field()
    product_amount = scrapy.Field()
    product_page_total = scrapy.Field()
    key_words = scrapy.Field()

class ProductPageItem(scrapy.Item): 
    manufacture_name = scrapy.Field()
    europe_page_url = scrapy.Field()
    product_links = scrapy.Field()

class ProductDetailItem(scrapy.Item): 
    # Maybe need
    manufacture_name = scrapy.Field()
    europe_page_url = scrapy.Field()

    # Definitely need
    product_name = scrapy.Field()
    product_image_link = scrapy.Field()
    product_url = scrapy.Field()
    product_description = scrapy.Field()
    product_keywords = scrapy.Field()

class ProductImageItem(scrapy.Item): 
    manufacture_name = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_pipeline_item = scrapy.Field()


