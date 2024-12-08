from scrapeNews.items import ArticleKlanItem, ArticleRtshItem, TopChannelItem
from scrapeNews.models import ArticleKlan, ArticleRtsh, engine, ArticleTopChannel
from sqlalchemy.orm import sessionmaker


class MySQLPipeline:
    def __init__(self):
        self.session = None
        self.Session = None

    def open_spider(self, spider):
        """
        Called when the spider is opened.
        """
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

    def close_spider(self, spider):
        """
        Called when the spider is closed.
        """
        if hasattr(self, "session"):
            self.session.close()

    def process_item(self, item, spider):
        try:
            if isinstance(item, ArticleKlanItem):
                spider.logger.info(f"Processing Klan article: {item['article_title']}")

                existing_article = (
                    self.session.query(ArticleKlan)
                    .filter_by(article_title=item['article_title'])
                    .first()
                )
                if not existing_article:
                    article = ArticleKlan(
                        article_title=item['article_title'],
                        article_link=item['article_link'],
                        article_description=item.get('article_description', ''),
                        time_of_post=item.get('time_of_post', ''),
                        category=item.get('category', ''),
                        article_body=item.get('article_body', ''),
                        image_url=item.get('image_url', ''),
                    )
                    self.session.add(article)
                    self.session.commit()
                return item

            elif isinstance(item, ArticleRtshItem):
                spider.logger.info(f"Processing RTSH article: {item['article_title']}")

                existing_article = (
                    self.session.query(ArticleRtsh)
                    .filter_by(article_title=item['article_title'])
                    .first()
                )
                if not existing_article:
                    article = ArticleRtsh(
                        article_title=item['article_title'],
                        article_link=item['article_link'],
                        article_description=item.get('article_description', ''),
                        time_of_post=item.get('time_of_post', ''),
                        category=item.get('category', ''),
                        article_body=item.get('article_body', ''),
                        image_url=item.get('image_url', ''),
                    )
                    self.session.add(article)
                    self.session.commit()
                return item

            elif isinstance(item, TopChannelItem):
                spider.logger.info(f"Processing Top Channel article: {item['article_title']}")

                # Convert category list to a comma-separated string
                category = ', '.join(item.get('category', []))  # Default to an empty list if `category` is missing

                # Check if the article already exists in the database
                existing_article = (
                    self.session.query(ArticleTopChannel)
                    .filter_by(article_title=item['article_title'])
                    .first()
                )
                if not existing_article:
                    # Create a new ArticleTopChannel object and add it to the database
                    article = ArticleTopChannel(
                        article_title=item['article_title'],
                        article_link=item['article_link'],
                        article_description=item.get('article_description', ''),
                        time_of_post=item.get('time_of_post', ''),
                        category=category,  # Save the category as a string
                        article_body=item.get('article_body', ''),
                        image_url=item.get('image_url', ''),
                    )
                    self.session.add(article)
                    self.session.commit()
                return item

        except Exception as e:
            self.session.rollback()  # Rollback if there's an error
            spider.logger.error(f"Error processing item: {e}")
            raise e

