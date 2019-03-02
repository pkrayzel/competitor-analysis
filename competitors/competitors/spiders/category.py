import scrapy
import logging
from datetime import datetime

from competitors.common import FonqCompetitor, FlindersCompetitor

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

