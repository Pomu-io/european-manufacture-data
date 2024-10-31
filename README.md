# European manufacture - Scrapy + Splash (Lua)

## Common Links

### Main directory page

https://www.europages.co.uk/

### Scraping categories: apparel

https://www.europages.co.uk/en/search?q=apparel

### Sample manufacture page

#### Comprehensive information

https://www.europages.co.uk/GS7-CO/00000005449388-790690001.html

#### Lack of information

##### Directory page

https://www.europages.co.uk/companies/pg-75/apparel.html

##### One Example

https://www.europages.co.uk/KENDAL-BED-CENTRE/00000004257213-001.html

## Common Commands

### Virtual Environment

'''
python3 -m venv myenv
'''
'''
source myenv/bin/activate
'''

### Run the project

You can change "filename" and "output.json", modify "LOG_LEVEL" variable to 5 different levels to display level of information. Details here: https://docs.scrapy.org/en/2.11/topics/logging.html

`scrapy crawl spider_name -o LOGS/fashion_output_$(date +%Y%m%d*%H%M%S).json -s LOG_FILE=LOGS/fashion_log_$(date +%Y%m%d\_%H%M%S).txt -s LOG_LEVEL=DEBUG`

`scrapy crawl perManufacture -o LOGS/fashion_output_$(date +%Y%m%d*%H%M%S).json -s LOG_FILE=LOGS/fashion_log_$(date +%Y%m%d\_%H%M%S).txt -s LOG_LEVEL=DEBUG`

#### Log Levels

logging.CRITICAL - for critical errors (highest severity)

logging.ERROR - for regular errors

logging.WARNING - for warning messages

logging.INFO - for informational messages

logging.DEBUG - for debugging messages (lowest severity)

### Git operations

#### if gitignore some file:

`git check-ignore + filename`

### Database operations

#### Open and connect to postgres

`psql -U postgres`

#### Back up database

example:
`pg_dump -U postgres -d DATABASE_NAME -F c -b -v -f /Users/liuqiming/Desktop/pomu/europeanManufacture/manufacture_name_url.dump`

take-away:
`pg_dump -U postgres -d europe_manufactures -F c -b -v -f /Users/liuqiming/Desktop/pomu/europeanManufacture/manufacture_name_url.dump`

## Usage

### Different search directory changing

1. To change different directory, modify `TABLE_NAME` variable in `seetings.py`, this will create a new table in current database

2. In `EuropeanManufactureSpider.py`,
   (1) change `url` variable
   (2) change for loop range

####

### Database connection

refer to article about scrapy and postgres
https://scrapeops.io/python-scrapy-playbook/scrapy-save-data-postgres/

### Drafts

response.xpath("//h2[@class='title no-margin font-display-500 col-span-1 md:col-span-2 order-2']/text()").get()
