import scrapy
from scrapeNews.items import ArticleKlanItem


class KlanSpider(scrapy.Spider):
    name = "klan"
    allowed_domains = ["tvklan.al"]
    start_urls = ["https://tvklan.al/lajme"]

    def parse(self, response):
        categories = response.css('.sub-menu a')
        for category in categories:
            name = category.css('::text').get().strip()
            link = category.css('::attr(href)').get()
            full_link = response.urljoin(link)

            yield scrapy.Request(full_link, callback=self.parse_category, meta={'category': name})

    def parse_category(self, response):
        category = response.meta['category']
        articles = response.css('.post-item .post-link')
        for article in articles:
            article_link = response.urljoin(article.css('::attr(href)').get())
            yield scrapy.Request(article_link, callback=self.parse_article, meta={'category': category})

    def parse_article(self, response):
        category = response.meta['category']
        # Extract article title
        title = response.css('.post-title-wrapper h1.post-title::text').get()
        image = response.css(".fit-img-wrapper img::attr(src)").get()
        # Extract publish time
        publish_time = response.css('.published-time::text').get()
        # Extract main content paragraphs
        content_paragraphs = response.css('.post-content p::text').getall()
        content = ' '.join(content_paragraphs)

        item = ArticleKlanItem()
        item['article_title'] = title
        item['article_link'] = response.url
        item['time_of_post'] = publish_time
        item['category'] = category
        item['article_body'] = content
        item['image_url'] = image
        item['channel'] = 'Klan HD'
        yield item