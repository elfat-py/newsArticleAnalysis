from scrapeNews.items import ArticleKlanItem, ArticleRtshItem
from scrapeNews.models import ArticleKlan, ArticleRtsh, engine
from sqlalchemy.orm import sessionmaker


class MySQLPipeline:
    def __init__(self):
        self.session = None
        self.Session = None

    def open_spider(self, spider):
        """Called when the spider is opened."""
        # Initialize the database session
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

    def close_spider(self, spider):
        """Called when the spider is closed."""
        # Close the database session
        if hasattr(self, "session"):
            self.session.close()

    def process_item(self, item, spider):
        if isinstance(item, ArticleKlanItem):
            """Called for each item pipeline component."""
            if isinstance(item, ArticleKlanItem):
                # Print the item being processed
                spider.logger.info(f"Processing item: {item['article_title']}")

                # Check if the article already exists in the database
                existing_article = (
                    self.session.query(ArticleKlan)
                    .filter_by(article_title=item['article_title'])
                    .first()
                )
                if not existing_article:
                    # Create a new Article object and add it to the database
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

        elif isinstance(item, ArticleRtshItem):
            # Handle ArticleRtshItem
            spider.logger.info(f"Processing RTSH article: {item['title']}")

            # Check if the article already exists in the database
            existing_article = (
                self.session.query(ArticleRtsh)
                .filter_by(article_title=item['title'])
                .first()
            )
            if not existing_article:
                # Create a new ArticleRtsh object and add it to the database
                article = ArticleRtsh(
                    article_title=item['title'],
                    article_link=item['link'],
                    article_description=item['description'],
                    time_of_post=item['time_of_post'],
                    category=item['category'],
                    article_body=item['content'],
                    image_url=item['image_url'],
                )
                self.session.add(article)
                self.session.commit()

        return item

