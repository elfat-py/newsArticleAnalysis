import scrapy
from scrapeNews.items import ArticleRtshItem
import re


class RtshSpider(scrapy.Spider):
    name = 'rtsh'
    allowed_domains = ['lajme.rtsh.al']
    start_urls = ['https://lajme.rtsh.al/']

    # The reason we weren't able to scrape the website is because the website is using some kind of bot protection
    custom_settings = {
        'DOWNLOAD_DELAY': 1,  # Prevent overloading the server
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 1,
        'AUTOTHROTTLE_MAX_DELAY': 10   ,
        'ROBOTSTXT_OBEY': False,  # Ignore robots.txt
    }

    def parse(self, response):
        # Extract all category links
        category_links = response.css(".list-unstyled li a::attr(href)").getall()
        for link in category_links:
            absolute_link = response.urljoin(link)
            if "excluded-term" not in absolute_link:
                yield response.follow(
                    absolute_link,
                    callback=self.parse_category,
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'},
                )

    def parse_category(self, response):
        # Follow article links
        for article in response.css(".row .article"):
            article_link = article.css(".article-header a::attr(href)").get()
            if article_link:
                yield response.follow(
                    response.urljoin(article_link),
                    callback=self.parse_article,
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'},
                )

    def parse_article(self, response):
        # Extracts and clean time
        time_raw = response.css(".row > .col-lg-8 > p").get()
        if time_raw:
            match = re.search(r'\d{2}/\d{2}/\d{4}', time_raw)
            time_cleaned = match.group(0) if match else "Not specified"
        else:
            time_cleaned = "Not specified"

        # Extract other fields
        content = response.css(".article-content").get()
        title = response.css(".c-black::text").get() or "No title available"
        category = response.css(".category::text").get() or "Uncategorized"
        image = response.css(".article-figure > img::attr(src)").get() or "No image available"

        # Create the item
        item = ArticleRtshItem()
        item['article_title'] = title
        item['article_link'] = response.url
        item['time_of_post'] = time_cleaned  # Use cleaned time
        item['category'] = category
        item['article_body'] = content or "No content available"
        item['image_url'] = image
        item['channel'] = 'RTSH'

        yield item
