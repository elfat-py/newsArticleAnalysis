import scrapy


class RtshSpider(scrapy.Spider):
    allowed_domains = ["lajme.rtsh.al"]
    name = 'rtsh'
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
            # Exclude URIs that are in the excluded_uris list
            if not any(excluded in link for excluded in self.excluded_uris):
                # If the link is not excluded, follow it
                yield response.follow(link, callback=self.parse_category)

    def parse_category(self, response):
        # Logic for parsing the category page
        self.log(f"Processing category: {response.url}")
