import aws_lambda_logging
from cerberus import Validator
import logging
import os
import scrapy
from scrapy.crawler import CrawlerProcess


from datetime import datetime

from competitor import find_competitor

aws_lambda_logging.setup(level='INFO', boto_level='CRITICAL')
logging.getLogger('urllib3').setLevel(logging.CRITICAL)


event_validator = Validator({
    "competitors": {
        "type": "list",
        "minlength": 1,
        "required": True,
        "schema": {
            "type": "dict",
            "schema": {
                "name": {
                    "type": "string",
                    "required": True
                },
                "country": {
                    "type": "string",
                    "required": True
                },
            }
        }
    },
})


class CategorySpider(scrapy.Spider):

    name = 'category'

    def __init__(self, competitors):
        self.competitors = competitors

    def start_requests(self):
        for c in self.competitors:
            competitor = find_competitor(name=c["name"], country=c["country"])

            for category, value in competitor.get_categories_urls().items():
                category_url = value['url']
                yield scrapy.Request(url=category_url,
                                     meta={
                                         'country': competitor.country,
                                         'competitor': competitor.name,
                                         'category': category,
                                         'category_url': category_url,
                                         'page_number': 1
                                     },
                                     callback=self.parse_first_page)

    def parse_first_page(self, response):
        competitor = find_competitor(name=response.meta['competitor'], country=response.meta['country'])
        category_details = competitor.parse_category_details(response)
        # yield the first page result
        yield category_details

        next_pages = competitor.get_next_pages_for_category(category_details)

        for (url, meta) in next_pages:
            yield scrapy.Request(url=url, meta=meta, callback=self.parse_next_page)

    def parse_next_page(self, response):
        competitor = find_competitor(name=response.meta['competitor'], country=response.meta['country'])
        yield competitor.parse_category_details(response)

    def closed(self, reason):
        stats = self.crawler.stats.get_stats()
        start_time = stats.get("start_time")
        end_time = datetime.utcnow()
        difference = end_time - start_time
        self.logger.info(f"Total scraping time: {difference} seconds")


def main(competitors):
    error_messages = []
    try:
        bucket_name = os.getenv('BUCKET_NAME', 'made-dev-competitor-analysis')

        date_string = datetime.now().strftime('%Y-%m-%d')

        keys = list(map(lambda c: f'{c["country"]}_{c["name"]}', competitors))
        key = "_".join(keys)

        process = CrawlerProcess({
            "LOG_LEVEL": "ERROR",
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'FEED_FORMAT': 'json',
            'FEED_URI': f's3://{bucket_name}/category-overall-info/{date_string}/{key}.json'
        })

        process.crawl(CategorySpider, competitors=competitors)
        process.start()

    except Exception as e:
        error_message = f"Error for {competitors}: - {e}"
        logging.error(error_message)
        error_messages.append(error_message)

    return {
        "result": "success",
        "error_count": len(error_messages),
        "error_messages": error_messages
    }


def handler(event, context):
    is_valid = event_validator.validate(event)

    if not is_valid:
        return {
            "result": "error",
            "error_message": f"Wrong input - {event_validator.errors}"
        }

    return main(event["competitors"])
