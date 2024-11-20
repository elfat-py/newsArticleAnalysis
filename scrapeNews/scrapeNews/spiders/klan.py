import scrapy
from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from scrapeNews.items import ArticleKlan

# Replace with your actual MySQL credentials and database name
engine = create_engine('mysql+mysqlconnector://root:elgert1234@localhost:3307/news_db')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
# Define the Article model
class Article(Base):
    __tablename__ = 'articles_klan'
    article_title = Column(String(255), primary_key=True)  # Specify length for VARCHAR
    article_link = Column(String(255))
    article_description = Column(Text)
    time_of_post = Column(String(50))  # Adjust length as needed
    category = Column(String(100))     # Adjust length as needed
    article_body = Column(Text)
    image_url = Column(String(255))

Base.metadata.create_all(engine)


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

        # Extract publish time
        publish_time = response.css('.published-time::text').get()

        # Extract reading time if available
        reading_time = response.css('.reading-time::text').get()

        # Extract related articles
        related_articles = []
        related_items = response.css('.content-related-wrapper .related ul li a')
        for item in related_items:
            related_title = item.css('h3::text').get()
            related_link = response.urljoin(item.css('::attr(href)').get())
            related_articles.append({'title': related_title, 'link': related_link})

        # Extract main content paragraphs
        content_paragraphs = response.css('.post-content p::text').getall()
        content = ' '.join(content_paragraphs)

        item = ArticleKlan()
        item['article_title'] = title
        item['article_link'] = response.url
        item['article_description'] = ''
        item['time_of_post'] = publish_time
        item['category'] = category
        item['article_body'] = content
        item['image_url'] = ''

        # Save the article to the database
        # article_data = {
        #     "article_title": title,
        #     "article_link": response.url,
        #     "article_description": "",
        #     "time_of_post": publish_time,
        #     "category": category,
        #     "article_body": content,
        #     "image_url": "",
        # }
        # self.save_to_db(article_data)

    def save_to_db(self, article_data):
        # Create an Article object and save to the database
        article = Article(
            article_title=article_data.get("article_title"),
            article_link=article_data.get("article_link"),
            article_description=article_data.get("article_description"),
            time_of_post=article_data.get("time_of_post"),
            category=article_data.get("category"),
            article_body=article_data.get("article_body"),
            image_url=article_data.get("image_url"),
        )
        session.add(article)
        session.commit()
