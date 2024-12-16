import scrapy
from scrapeNews.items import TopChannelItem


class TopchannelSpider(scrapy.Spider):
    name = "topja"  # Spider name
    allowed_domains = ["top-channel.tv"]  # Allowed domain to scrape
    start_urls = ["https://top-channel.tv/"]  # Starting URL

    def parse(self, response):
        # List of CSS selectors for categories
        categoryList = ['#newsMenu1', '#newsMenu2']

        for category in categoryList:
            categoryLinks = response.css(f"{category} .menu-item > a::attr(href)").getall()
            for link in categoryLinks:
                yield scrapy.Request(link, callback=self.parse_category)

    def parse_category(self, response):
        main = response.css('#main')
        articles = main.css('.article > a::attr(href)').getall()

        for article_link in articles:
            print(f"Article Link: {article_link}")
            yield scrapy.Request(article_link, callback=self.parse_article)

    def parse_article(self, article):
        title = article.css("div.title h1::text").get()
        categories = article.css("div.categories a::text").getall()
        content = " ".join(article.css("div.articleContent p::text").getall())
        image_url = article.css("div.featuredImageContainer img::attr(src)").get()

        item = TopChannelItem()
        item["article_title"] = title
        item["article_link"] = article.url
        item["category"] = categories
        item["article_body"] = content
        item["image_url"] = image_url
        item['channel'] = 'TOP Channel'

        yield item
