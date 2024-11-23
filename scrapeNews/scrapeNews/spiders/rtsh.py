import scrapy
from scrapeNews.items import ArticleRtshItem

class RtshSpider(scrapy.Spider):
    name = 'rtsh'
    allowed_domains = ['lajme.rtsh.al']
    start_urls = ['https://lajme.rtsh.al/']

    excluded_uris = [
        '/kuzhine',
        '/lifestyle',
        '/euro-2024-',
        '/paris-2024',
        'https://www.facebook.com/RadioTelevizioniShqiptarRTSH',
        'https://www.instagram.com/rtsh.official',
        'https://www.youtube.com/channel/UC6tAjIpd8AWLI4ErBpBh2qg'
    ]

    def parse(self, response):
        # Extract all category links
        category_links = response.css('a::attr(href)').getall()

        for link in category_links:
            absolute_link = response.urljoin(link)
            # Exclude URIs that are in the excluded_uris list
            if not any(excluded in absolute_link for excluded in self.excluded_uris):
                self.log(f"Following link: {absolute_link}")
                yield response.follow(absolute_link, callback=self.parse_category)
            else:
                self.log(f"Excluded link: {absolute_link}")

    def parse_category(self, response):
        category = response.meta.get('category', 'Uncategorized')
        article_links = response.css('a.article-link::attr(href)').getall()

        for link in article_links:
            absolute_link = response.urljoin(link)
            yield response.follow(absolute_link, callback=self.parse_article, meta={'category': category})

        next_page = response.css('a.next-page::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield response.follow(next_page_url, callback=self.parse_category, meta={'category': category})

    def parse_article(self, response):
        category = response.meta.get('category', 'Uncategorized')
        title = response.css('h1.c-black text-bold h2::text').get()
        publish_time = response.css('p.col-lg-8::text').get()
        content_paragraphs = response.css('div.article-content mb-32::text').getall()
        content = ' '.join(content_paragraphs)
        image_url = response.css('img.article-figure::attr(src)').get()

        item = ArticleRtshItem()
        item['title'] = title
        item['link'] = response.url
        item['description'] = ''  # Add description logic if needed
        item['time_of_post'] = publish_time
        item['category'] = category
        item['content'] = content
        item['image_url'] = image_url
        yield item