import asyncio
from fastapi import FastAPI
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import asyncioreactor, defer
from twisted.internet.defer import ensureDeferred, DeferredList
from scrapeNews.spiders.klan import KlanSpider
from scrapeNews.spiders.rtsh import RtshSpider
from scrapeNews.spiders.topChannel import TopchannelSpider

# Install asyncio-compatible reactor
try:
    asyncioreactor.install()
except Exception:
    pass  # Reactor can only be installed once

# Initialize FastAPI
app = FastAPI()

# Configure Scrapy logging
configure_logging()

# Scrapy Runner
runner = CrawlerRunner()

@app.get("/")
async def run_spiders():

    try:
        # Collect all the Deferreds into a list
        deferreds = [
            runner.crawl(KlanSpider),
            runner.crawl(TopchannelSpider),
            runner.crawl(RtshSpider),
        ]

        # Use DeferredList to manage multiple Deferreds
        await ensureDeferred(DeferredList(deferreds, fireOnOneErrback=True))
        return {"status": "Crawling completed successfully"}
    except Exception as e:
        return {"status": "Error", "details": str(e)}

# Run FastAPI server only when executing this file directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
