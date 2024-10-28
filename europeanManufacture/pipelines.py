# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import datetime
import psycopg2

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

    keys = [
    "Manufacture Name",  # corresponds to 'name'
    "Url",               # corresponds to 'europe_page_url'
    "About Us",          # corresponds to 'about_us'
    "Company Website",   # corresponds to 'company_website'
    "Country",           # corresponds to 'country'
    "Delivery",          # corresponds to 'delivery'
    "Employee Number",   # corresponds to 'employee_number'
    "Founded Time",      # corresponds to 'founded_time'
    "Key Words",         # corresponds to 'key_words'
    "Location",          # corresponds to 'location'
    "Phone Number",      # corresponds to 'phone_number'
    "Product Amount",    # corresponds to 'product_amount'
    "Product Page Total",# corresponds to 'product_page_total'
    "Supplier Type"      # corresponds to 'supplier_type'
]

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
        return item

    def close_spider(self, spider): 
        print(f"Finish writing to database. Closing at {datetime.datetime.now()}\n")
        self.cur.close()
        self.connection.close()

    @classmethod
    def from_crawler(cls, crawler):
        # Get table_name from settings or default to 'apparel_name_url'
        table_name = crawler.settings.get('WRITE_TO_TABLE_NAME', 'apparel_manufactures')
        return cls(table_name=table_name)

