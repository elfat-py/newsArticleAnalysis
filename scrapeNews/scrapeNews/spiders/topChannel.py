import scrapy


class TopchannelSpider(scrapy.Spider):
    name = "topja"
    allowed_domains = ["top-channel.tv"]
    start_urls = ["https://top-channel.tv/"]

    def parse(self, response):
        categories = [response.css('#newsMenu1'), response.css('#newsMenu2')]  # Combine categories
        #response.css("#newsMenu1 > .menu-item > a::attr(href)").getall()
        for category in categories:
            name = category.css('::text').get().strip()
            link = category.css('::attr(href)').get()
            full_link = response.urljoin(link)

            yield name, full_link, link
