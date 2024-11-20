# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapeNews.items import ArticleKlan
from scrapeNews.models import ArticleKlan, engine
from sqlalchemy.orm import sessionmaker

class ScrapenewsPipeline:
    def process_item(self, item, spider):
        return item

class MySQLPipeline:
    def open_spider(self, spider):
        # Initialize the database session
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

    def close_spider(self, spider):
        # Close the database session
        self.session.close()

    def process_item(self, item, spider):
        print('Processing item:', item['article_title'])
        return True
        existing_article = self.session.query(ArticleKlan).filter_by(article_title=item['article_title']).first()
        if not existing_article:
            # Create a new Article object and add it to the session
            article = ArticleKlan(
                article_title=item['article_title'],
                article_link=item['article_link'],
                article_description=item['article_description'],
                time_of_post=item['time_of_post'],
                category=item['category'],
                article_body=item['article_body'],
                image_url=item['image_url'],
            )
            self.session.add(article)
            self.session.commit()

        return item