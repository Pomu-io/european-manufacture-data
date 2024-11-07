# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import datetime
import time
import psycopg2
from scrapy.pipelines.images import ImagesPipeline
import os
from scrapy import Request
from europeanManufacture.items import ProductDetailItem, ProductImageItem

# This class is for scaping manufacture directories. use or disable it in settings.py 
class EuropeanManufactureNameURLPipeline:

    keys = ["Manufacture Name", "Url"]
    csv_name = ""

    def __init__(self, table_name='apparel_name_url'):
        ## Connection Details
        hostname = 'localhost'
        username = 'postgres'
        password = 'qiming1021' # your password
        database = 'europe_manufactures'

        self.table_name = table_name

        ## Create/Connect to database
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        
        ## Create cursor, used to execute commands
        self.cur = self.connection.cursor()
        
        ## Create quotes table if none exists
        self.cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id serial PRIMARY KEY, 
                manufacture_name VARCHAR(255),
                url TEXT
            )
            """)

    def process_item(self, item, spider):
        self.cur.execute(f"""
        insert into {self.table_name} (manufacture_name, url) values (%s, %s)
        """, (item['name'], item['url']))
        self.connection.commit()
        return item

    def close_spider(self, spider): 
        print(f"Finish writing to database. Closing at {datetime.datetime.now()}\n")
        self.cur.close()
        self.connection.close()

    @classmethod
    def from_crawler(cls, crawler):
        # Get table_name from settings or default to 'apparel_name_url'
        table_name = crawler.settings.get('WRITE_TO_TABLE_NAME', 'apparel_name_url')
        return cls(table_name=table_name)
    
class PerEuropeanManufacturePipeline: 

    def __init__(self, table_name='apparel_name_url'):
        ## Connection Details
        hostname = 'localhost'
        username = 'postgres'
        password = 'qiming1021' # your password
        database = 'europe_manufactures'

        self.table_name = table_name

        ## Create/Connect to database
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        
        ## Create cursor, used to execute commands
        self.cur = self.connection.cursor()

        self.cur.execute("ROLLBACK")
        
        ## Create quotes table if none exists
        self.cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
            id serial PRIMARY KEY,
            manufacture_name VARCHAR(255),
            europe_page_url TEXT,
            company_website TEXT,
            location VARCHAR(255),
            country VARCHAR(100),
            phone_number VARCHAR(50),
            VAT_number VARCHAR(50),
            average_response_time VARCHAR(50),
            average_response_rate VARCHAR(50),
            delivery VARCHAR(255),
            founded_time VARCHAR(50),
            employee_number VARCHAR(50),
            supplier_type VARCHAR(255),
            about_us TEXT,
            product_amount INTEGER,
            product_page_total INTEGER,
            key_words TEXT
        )
            """)

    def process_item(self, item, spider):
        try: 
            self.cur.execute(f"""
            INSERT INTO {self.table_name} (
                manufacture_name, europe_page_url, company_website, location, country,
                phone_number, VAT_number, average_response_time, average_response_rate,
                delivery, founded_time, employee_number, supplier_type, about_us,
                product_amount, product_page_total, key_words
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
                item.get('name'),
                item.get('europe_page_url'),
                item.get('company_website'),
                item.get('location'),
                item.get('country'),
                item.get('phone_number'),
                item.get('VAT_number'),
                item.get('average_response_time'),
                item.get('average_response_rate'),
                item.get('delivery'),
                item.get('founded_time'),
                item.get('employee_number'),
                item.get('supplier_type'),
                item.get('about_us'),
                item.get('product_amount'),
                item.get('product_page_total'),
                item.get('key_words')
            ))
            self.connection.commit()
        except psycopg2.DatabaseError as e:
            spider.logger.error(f"Error inserting item into database: {e}")
            self.connection.rollback()
        except Exception as e:
            spider.logger.error(f"Unexpected error: {e}")
        return item

    def close_spider(self, spider): 
        print(f"Finish writing to database. Closing at {datetime.datetime.now()}\n")
        self.cur.close()
        self.connection.close()

    @classmethod
    def from_crawler(cls, crawler):
        # Get table_name from settings or default to 'apparel_name_url'
        table_name = crawler.settings.get('PER_MANUFACTURE_WRITE_TO_TABLE_NAME', 'apparel_manufactures')
        return cls(table_name=table_name)

class PerEuropeanManufacturePipelineNo2: 

    def __init__(self, table_name='apparel_name_url'):
        ## Connection Details
        hostname = 'localhost'
        username = 'postgres'
        password = 'qiming1021' # your password
        database = 'europe_manufactures'

        self.table_name = table_name

        ## Create/Connect to database
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        
        ## Create cursor, used to execute commands
        self.cur = self.connection.cursor()

        self.cur.execute("ROLLBACK")
        
        ## Create quotes table if none exists
        self.cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
            id serial PRIMARY KEY,
            manufacture_name VARCHAR(255),
            europe_page_url TEXT,
            company_website TEXT,
            location VARCHAR(255),
            country VARCHAR(100),
            phone_number VARCHAR(50),
            VAT_number VARCHAR(50),
            average_response_time VARCHAR(50),
            average_response_rate VARCHAR(50),
            delivery VARCHAR(255),
            founded_time VARCHAR(50),
            employee_number VARCHAR(50),
            supplier_type VARCHAR(255),
            about_us TEXT,
            product_amount INTEGER,
            product_page_total INTEGER,
            key_words TEXT
        )
            """)

    def process_item(self, item, spider):
        try: 
            self.cur.execute(f"""
            INSERT INTO {self.table_name} (
                manufacture_name, europe_page_url, company_website, location, country,
                phone_number, VAT_number, average_response_time, average_response_rate,
                delivery, founded_time, employee_number, supplier_type, about_us,
                product_amount, product_page_total, key_words
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
                item.get('name'),
                item.get('europe_page_url'),
                item.get('company_website'),
                item.get('location'),
                item.get('country'),
                item.get('phone_number'),
                item.get('VAT_number'),
                item.get('average_response_time'),
                item.get('average_response_rate'),
                item.get('delivery'),
                item.get('founded_time'),
                item.get('employee_number'),
                item.get('supplier_type'),
                item.get('about_us'),
                item.get('product_amount'),
                item.get('product_page_total'),
                item.get('key_words')
            ))
            self.connection.commit()
        except psycopg2.DatabaseError as e:
            spider.logger.error(f"Error inserting item into database: {e}")
            self.connection.rollback()
        except Exception as e:
            spider.logger.error(f"Unexpected error: {e}")
        return item

    def close_spider(self, spider): 
        print(f"Finish writing to database. Closing at {datetime.datetime.now()}\n")
        self.cur.close()
        self.connection.close()

    @classmethod
    def from_crawler(cls, crawler):
        # Get table_name from settings or default to 'apparel_name_url'
        table_name = crawler.settings.get('No2_PER_MANUFACTURE_WRITE_TO_TABLE_NAME', 'fashion_manufactures')
        return cls(table_name=table_name)


class ProductImagePipeline(ImagesPipeline):

    print("\n--------------- In ProductImagePipeline ---------------\n")

    def file_path(self, request, response=None, info=None, *, item=None):
        # Retrieve manufacture name and format it for a directory name
        product_name = request.meta.get('product_name', 'default_product').replace(' ', '_').replace('/', '_')
        manufacture_name = request.meta.get('manufacture_name', 'default_name').replace(' ', '_').replace('/', '_')
        
        # Create a subdirectory for the manufacture and set the image file name
        # print(f"file path is: {manufacture_name}/{product_name}\n")
        return f"{manufacture_name}/{product_name}.jpg"

    def get_media_requests(self, item, info):
        if not isinstance(item, ProductImageItem): 
            return item
        # print("\n--------------- In pipeline function 'get_media_requests' ---------------\n")
        # Pass manufacture name to the request for use in file_path
        # print(f"manufacture_name obtained from item: {item.get('manufacture_name')} ")
        # print(f"what is image_pipeline_item again? \n {item.get('image_pipeline_item')}")
        for product_name, image_url in item.get('image_pipeline_item').items():
            # print(f"Getting the request for {product_name} with url {image_url}\n")
            yield Request(image_url, meta={'product_name': product_name, 'manufacture_name': item.get('manufacture_name')})


class ProductLinksPipeline: 

    def __init__(self, table_name=''):
        ## Connection Details
        hostname = 'localhost'
        username = 'postgres'
        password = 'qiming1021' # your password
        database = 'europe_manufactures'

        self.table_name = table_name
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)     
        self.cur = self.connection.cursor()
        self.cur.execute("ROLLBACK")
        
        self.cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
            id serial PRIMARY KEY,
            manufacture_name VARCHAR(255),
            europe_page_url TEXT,
            product_links TEXT
        )
            """)

    def process_item(self, item, spider):

        print(f"In pipeline processing_item, the item is {item}")

        try: 
            product_links_str = ', '.join(item.get('product_links'))
            self.cur.execute(f"""
            INSERT INTO {self.table_name} (
                manufacture_name, europe_page_url, product_links
            ) VALUES (%s, %s, %s)
        """, (
                item.get('manufacture_name'),
                item.get('europe_page_url'),
                product_links_str
            ))
            self.connection.commit()
        except psycopg2.DatabaseError as e:
            spider.logger.error(f"Error inserting item into database: {e}")
            self.connection.rollback()
        except Exception as e:
            spider.logger.error(f"Unexpected error: {e}")
        return item

    def close_spider(self, spider): 
        print(f"Finish writing to database. Closing at {datetime.datetime.now()}\n")
        self.cur.close()
        self.connection.close()

    @classmethod
    def from_crawler(cls, crawler):
        # Get table_name from settings or default to 'apparel_name_url'
        table_name = crawler.settings.get('PRODUCT_LINKS_WRITE_TO_TABLE_NAME', 'PRODUCT_LINKS_WRITE_TO_TABLE_NAME')
        return cls(table_name=table_name)

class ProductDetailPipeline: 

    def __init__(self, table_name=''):
        ## Connection Details
        hostname = 'localhost'
        username = 'postgres'
        password = 'qiming1021' 
        database = 'europe_manufactures'

        self.table_name = table_name
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)     
        self.cur = self.connection.cursor()
        self.cur.execute("ROLLBACK")
        
        self.cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
            id serial PRIMARY KEY,
            manufacture_name VARCHAR(255),
            europe_page_url TEXT
        )
            """)

    def process_item(self, item, spider):

        if not isinstance(item, ProductDetailItem):
            # print(f"item is of type {type(item)}")
            return item

        # print(f"In pipeline processing_item, the item is {item}")

        try: 
            item_length = len(item.get('product_name'))
            self.cur.execute(f"""
            INSERT INTO {self.table_name} (
                manufacture_name, europe_page_url
            ) VALUES (%s, %s)
            """, (item.get('manufacture_name'), item.get('europe_page_url')))
            for i in range (1, item_length):
                self.cur.execute(f"""
                    do $$
                        begin
                            if not exists (
                                SELECT 1 FROM information_schema.columns 
                                where table_name = '{self.table_name}'
                                and column_name = 'product_{i}_name'
                            ) then
                                alter table {self.table_name}
                                add column product_{i}_name text null;
                                alter table {self.table_name}
                                add column product_{i}_url text null;
                                alter table {self.table_name}
                                add column product_{i}_description text null;
                                alter table {self.table_name}
                                add column product_{i}_keywords text null; 
                                alter table {self.table_name}
                                add column product_{i}_image_link text null; 
                            end if;
                    end $$;
                    """)
                # print(f"item.get('product_name') is \n{item.get('product_name')}\n")
                for key, value in item.get('product_name').items(): 
                    # print(f"key is {key}, value is {value}")
                    if key == f'product_{i}_name': 
                        self.cur.execute(f"""update {self.table_name} set product_{i}_name=%s where manufacture_name=%s """, (value, item['manufacture_name']))
                # print(f"item.get('product_url') is \n{item.get('product_url')}\n")
                for key, value in item.get('product_url').items(): 
                    if key == f'product_{i}_url':
                        self.cur.execute(f"""update {self.table_name} set product_{i}_url=%s where manufacture_name=%s""", (value, item['manufacture_name']))
                # print(f"item.get('product_description') is \n{item.get('product_description')}\n")
                for key, value in item.get('product_description').items(): 
                    if key == f'product_{i}_description':
                        self.cur.execute(f"""update {self.table_name} set product_{i}_description=%s where manufacture_name=%s""", (value, item['manufacture_name']))
                # print(f"item.get('product_keywords') is \n{item.get(f'product_keywords')}\n")
                for key, value in item.get('product_keywords').items(): 
                    if key == f'product_{i}_keywords':
                        self.cur.execute(f"""update {self.table_name} set product_{i}_keywords=%s where manufacture_name=%s""", (value, item['manufacture_name']))
                # print(f"item.get('product_image_link') is \n{item.get(f'product_image_link')}\n")
                for key, value in item.get('product_image_link').items(): 
                    if key == f'product_{i}_image_link':
                        self.cur.execute(f"""update {self.table_name} set product_{i}_image_link=%s where manufacture_name=%s""", (value, item['manufacture_name']))
            
            self.connection.commit()
        except psycopg2.DatabaseError as e:
            spider.logger.error(f"Error inserting item into database: {e}")
            self.connection.rollback()
        except Exception as e:
            spider.logger.error(f"Unexpected error: {e}")
        return item

    def close_spider(self, spider): 
        print(f"Finish writing to database in ProductDetailPipeline. Closing at {datetime.datetime.now()}\n")
        self.cur.close()
        self.connection.close()

    @classmethod
    def from_crawler(cls, crawler):
        # Get table_name from settings or default to 'apparel_name_url'
        table_name = crawler.settings.get('PRODUCT_DETAILS_WRITE_TO_TABLE_NAME', 'apparel_manufacture_product_details')
        return cls(table_name=table_name)

