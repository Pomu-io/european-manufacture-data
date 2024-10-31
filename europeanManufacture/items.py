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

class ProductItem(scrapy.Item): 
    # Maybe need
    manufacture_name = scrapy.Field()
    europe_page_url = scrapy.Field()

    # Definitely need
    product_name_full = scrapy.Field()
    product_discription = scrapy.Field()
    product_key_word = scrapy.Field()

