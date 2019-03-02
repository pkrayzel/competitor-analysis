import scrapy
from scrapy.crawler import CrawlerProcess

import logging
from datetime import datetime

from common import FonqCompetitor, FlindersCompetitor

logger = logging.getLogger('category')

COMPETITORS = [
    FonqCompetitor(),
    FlindersCompetitor()
]


def find_competitor(name):
    for c in COMPETITORS:
        if c.name == name:
            return c


class CategorySpider(scrapy.Spider):

    name = 'category'

    def start_requests(self):
        for competitor in COMPETITORS:
            for category, value in competitor.get_categories_urls().items():
                yield scrapy.Request(value['url'], meta={
                    'competitor': competitor.name,
                    'category': category
                })

    def parse(self, response):
        competitor = find_competitor(response.meta['competitor'])
        yield competitor.parse_category_details(response)

    def closed(self, reason):
        logger.info("==============================================")

        stats = self.crawler.stats.get_stats()
        start_time = stats.get("start_time")
        end_time = datetime.utcnow()
        difference = end_time - start_time
        logger.info(f"Total scraping time: {difference} seconds")
        logger.info("==============================================")


def handler(event, context):
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'FEED_FORMAT': 'json',
        'FEED_URI': 's3://made-competitor-analysis/category/output.json'
    })

    process.crawl(CategorySpider)
    process.start() # the script will block here until the crawling is finished


if __name__ == "__main__":
    handler('', '')
