# Scrapy settings for boss_zhipin_spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'boss_zhipin_spider'

SPIDER_MODULES = ['boss_zhipin_spider.spiders']
NEWSPIDER_MODULE = 'boss_zhipin_spider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#     "Cookie": "sid=sem; __zp_seo_uuid__=9c0e6ea5-821d-4cb0-bb0c-1de2cfc674a1; __g=sem; __l=r=https%3A%2F%2Fcn.bing.com%2F&l=%2Fwww.zhipin.com%2Fkunming%2F%3Fkeyword%3D589009904%26qhclickid%3D01e7145f8ec9b99d%26sid%3Dsem%26_ts%3D1636336768529&s=1&g=%2Fwww.zhipin.com%2Fkunming%2F%3Fkeyword%3D589009904%26qhclickid%3D01e7145f8ec9b99d%26sid%3Dsem%26_ts%3D1636336768529&s=3&friend_source=0; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1636336771; lastCity=100010000; acw_tc=0bdd343616363394473923319e01a303ef78ff0b28b4cad593094293af53df; __zp_stoken__=f573dOEdiMzRmQmV7Aww8X11qLStRQm06NVJ2dWdsET1SO1V%2BFFYxfDtuelN0azB%2BHntHdzZPehEwPWAACAc2aR4AHBwcJm12Jj1ZTzgFO1gnHANPKAxvCgpYUgcpQEk1XEJ1X0RnBRh4eWE%3D; __c=1636336771; __a=50968896.1627352716.1627352716.1636336771.13.2.12.12; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1636340561"
#     #   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#     #   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'boss_zhipin_spider.middlewares.BossZhipinSpiderSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'boss_zhipin_spider.middlewares.BossZhipinSpiderDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'boss_zhipin_spider.pipelines.BossZhipinSpiderPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
