import scrapy


class TopchannelSpider(scrapy.Spider):
    name = "topChannel"
    allowed_domains = ["top-channel.tv"]
    start_urls = ["https://top-channel.tv/"]

    def parse(self, response):
        pass
