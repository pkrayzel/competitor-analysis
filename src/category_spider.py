import os
import scrapy
from scrapy.crawler import CrawlerProcess

from datetime import datetime

from common import find_competitor, COMPETITORS


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
    bucket_name = os.getenv('BUCKET_NAME', 'made-dev-competitor-analysis')

    date_string = datetime.now().strftime('%Y%m%d%H%M')

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'FEED_FORMAT': 'json',
        'FEED_URI': f's3://{bucket_name}/category-overall-info/{date_string}.json'
    })

    process.crawl(CategorySpider)
    process.start()

    return {
        "result": "success"
    }

if __name__ == "__main__":
    handler('', '')
