from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

from scrapeNews.spiders.topChannel import TopchannelSpider
from scrapeNews.spiders.klan import KlanSpider
from scrapeNews.spiders.rtsh import RtshSpider

# TODO i think i am going to need to build some api to call this function from my laravel app
def runSpiders():
    print('hello world')
    process = CrawlerProcess(get_project_settings())
    process.crawl(KlanSpider)
    process.crawl(TopchannelSpider)
    process.crawl(RtshSpider)
    process.start()

if __name__ == '__main__':
    runSpiders()