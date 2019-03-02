import scrapy
from scrapy.crawler import CrawlerProcess

from datetime import datetime

import common

COMPETITORS = [
    common.FonqCompetitor(),
    common.FlindersCompetitor()
]


def find_competitor(name):
    for c in COMPETITORS:
        if c.name == name:
            return c


class CategorySpider(scrapy.Spider):

    name = 'category'

    custom_setting = {
        "LOG_LEVEL": "INFO"
    }

    def start_requests(self):
        for competitor in COMPETITORS:
            for category, value in competitor.get_categories_urls().items():
                yield scrapy.Request(value['url'], meta={
                    'country': competitor.country,
                    'competitor': competitor.name,
                    'category': category
                })

    def parse(self, response):
        competitor = find_competitor(response.meta['competitor'])
        yield competitor.parse_category_details(response)

    def closed(self, reason):
        stats = self.crawler.stats.get_stats()
        start_time = stats.get("start_time")
        end_time = datetime.utcnow()
        difference = end_time - start_time
        self.logger.info(f"Total scraping time: {difference} seconds")


def handler(event, context):
    bucket_name = event['bucket_name']
    date_string = datetime.now().strftime('%Y%m%d%H%M')

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'FEED_FORMAT': 'json',
        'FEED_URI': f's3://{bucket_name}/netherlands/{date_string}.json'
    })

    process.crawl(CategorySpider)
    process.start()

    return {
        "result": "success"
    }

if __name__ == "__main__":
    handler('', '')
