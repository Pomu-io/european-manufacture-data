# Scrapy settings for europeanManufacture project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import scrapy_splash

BOT_NAME = "europeanManufacture"

SPIDER_MODULES = ["europeanManufacture.spiders"]
NEWSPIDER_MODULE = "europeanManufacture.spiders"

# scrapy-splsh relevant settings
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

SPLASH_URL = 'http://localhost:8050'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.36"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 4

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
RANDOMIZE_DOWNLOAD_DELAY = True 
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 2
CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
  #  "europeanManufacture.middlewares.EuropeanmanufactureSpiderMiddleware": 543,
  'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
  #  "europeanManufacture.middlewares.EuropeanmanufactureDownloaderMiddleware": 543,
  # 'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
  #  "europeanManufacture.pipelines.EuropeanManufactureNameURLPipeline": 300,
  # "europeanManufacture.pipelines.ProductImagePipeline": 1,
  "europeanManufacture.pipelines.PerEuropeanManufacturePipeline": 300,
}

IMAGES_STORE = '../IMAGES'

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 1
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 10
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

#############  Database name Setting for perManufactureSpider  #############
# apparel_manufactures
PER_MANUFACTURE_WRITE_TO_TABLE_NAME = 'fashion_manufactures'
# apparel_name_url
PER_MANUFACTURE_READ_FROM_TABLE_NAME = 'fashion_name_url'

#############  Database name Setting for perManufactureSpider  #############
PRODUCT_LINKS_WRITE_TO_TABLE_NAME = 'apparel_manufactures'
PRODUCT_LINKS_READ_FROM_TABLE_NAME = 'apparel_manufactures_product_links'


# SPLASH_COOKIES_DEBUG is False by default. 
#   Set to True to enable debugging cookies in the SplashCookiesMiddleware. This option is similar to COOKIES_DEBUG for the built-in scarpy cookies middleware: it logs sent and received cookies for all requests.
# SPLASH_LOG_400 is True by default - 
#   it instructs to log all 400 errors from Splash. They are important because they show errors occurred when executing the Splash script. Set it to False to disable this logging.
# SPLASH_SLOT_POLICY is scrapy_splash.SlotPolicy.PER_DOMAIN 
#   (as object, not just a string) by default. It specifies how concurrency & politeness are maintained for Splash requests, and specify the default value for slot_policy argument for SplashRequest, which is described below.
SPLASH_SLOT_POLICY = scrapy_splash.SlotPolicy.PER_DOMAIN

