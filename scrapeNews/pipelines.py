from scrapeNews.items import ArticleKlanItem, ArticleRtshItem, TopChannelItem
from scrapeNews.models import engine, Articles
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

    def get_time_of_post(self, url):
        """
        Extract the time of post from the URL
        :param url:
        :return:
        """
        if not url:
            return ''  # Return an empty string if the URL is missing
        parts = url.split('/')
        if len(parts) >= 5:
            return '/'.join(parts[3:6])  # Join the year, month, and day
        return ''  # Return an empty string if the URL structure is invalid

    def process_item(self, item, spider):
        try:
            if isinstance(item, ArticleKlanItem):
                spider.logger.info(f"Processing Klan article: {item['article_title']}")

                existing_article = (
                    self.session.query(Articles)
                    .filter_by(article_title=item['article_title'])
                    .first()
                )
                if not existing_article:

                    article = Articles(
                        article_title=item['article_title'],
                        article_link=item['article_link'],
                        time_of_post=item.get('time_of_post', ''),
                        category=item.get('category', ''),
                        article_body=item.get('article_body', ''),
                        image_url=item.get('image_url', ''),
                        channel=item.get('channel', '')
                    )
                    self.session.add(article)
                    self.session.commit()
                return item

            elif isinstance(item, ArticleRtshItem):
                existing_article = (
                    self.session.query(Articles)
                    .filter_by(article_title=item['article_title'])
                    .first()
                )
                if not existing_article:
                    article = Articles(
                        article_title=item['article_title'],
                        article_link=item['article_link'],
                        time_of_post=item.get('time_of_post', ''),
                        category=item.get('category', ''),
                        article_body=item.get('article_body', ''),
                        image_url=item.get('image_url', ''),
                        channel=item.get('channel', ''),
                    )
                    self.session.add(article)
                    self.session.commit()
                return item

            elif isinstance(item, TopChannelItem):
                category = ', '.join(item.get('category', []))
                time_of_post = self.get_time_of_post(item.get('article_link', ''))

                existing_article = (
                    self.session.query(Articles)
                    .filter_by(article_title=item['article_title'])
                    .first()
                )
                if not existing_article:
                    article = Articles(
                        article_title=item['article_title'],
                        article_link=item['article_link'],
                        time_of_post=time_of_post,
                        category=category,
                        article_body=item.get('article_body', ''),
                        image_url=item.get('image_url', ''),
                        channel=item.get('channel', ''),
                    )
                    self.session.add(article)
                    self.session.commit()
                return item

        except Exception as e:
            self.session.rollback()  # Rollback if there's an error
            spider.logger.error(f"Error processing item: {e}")
            raise e

