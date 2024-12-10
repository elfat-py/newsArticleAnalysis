# Define here the models for your scraped items
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy

class ArticleKlanItem(scrapy.Item):
    article_title = scrapy.Field()
    article_link = scrapy.Field()
    time_of_post = scrapy.Field()
    category = scrapy.Field()
    article_body = scrapy.Field()
    image_url = scrapy.Field()
    channel = scrapy.Field()


class ArticleRtshItem(scrapy.Item):
    article_title = scrapy.Field()
    article_link = scrapy.Field()
    time_of_post = scrapy.Field()
    category = scrapy.Field()
    article_body = scrapy.Field()
    image_url = scrapy.Field()
    channel = scrapy.Field()


class TopChannelItem(scrapy.Item):
    article_title = scrapy.Field()
    article_link = scrapy.Field()
    time_of_post = scrapy.Field()
    category = scrapy.Field()
    article_body = scrapy.Field()
    image_url = scrapy.Field()
    channel = scrapy.Field()
