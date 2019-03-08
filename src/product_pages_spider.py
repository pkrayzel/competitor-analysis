import json
from cerberus import Validator
import os
import logging
import aws_lambda_logging
import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import datetime

from competitor import find_competitor

aws_lambda_logging.setup(level='INFO', boto_level='CRITICAL')
logging.getLogger('urllib3').setLevel(logging.CRITICAL)


event_validator = Validator({
    "Records": {
        "type": "list",
        "minlength": 1,
        "maxlength": 1,
        "required": True,
        "schema": {
            "type": "dict",
            "schema": {
                "messageId": { "type": "string", "required": True },
                "receiptHandle": { "type": "string", "required": True },
                "body": { "type": "string", "required": True },
                "attributes": { "type": "dict", "required": True },
                "messageAttributes": { "type": "dict", "required": True },
                "md5OfBody": { "type": "string", "required": True },
                "eventSource": { "type": "string", "required": True },
                "eventSourceARN": { "type": "string", "required": True },
                "awsRegion": { "type": "string", "required": True },
            }
        }
    },
})


class ProductPagesSpider(scrapy.Spider):

    name = 'product-pages'

    custom_settings = {
        "DOWNLOAD_DELAY": 2,
        "RETRY_TIMES": 10,
        "RETRY_HTTP_CODES": [500, 502, 503, 504, 400, 403, 404, 408]
    }

    def __init__(self, item=None):
        self.item = item

    def start_requests(self):
        for i, link in enumerate(self.item["product_links"]):

            yield scrapy.Request(link,
                                 meta={
                                     'country': self.item["country"],
                                     'competitor': self.item["competitor"],
                                     'category': self.item["category"],
                                     'category_url': self.item["category_url"],
                                     'page_url': link,
                                     'page_number': int(self.item["page_number"]),
                                     'product_number': i,
                                 })

    def parse(self, response):
        competitor = find_competitor(response.meta['competitor'])
        yield competitor.parse_product_detail(response)

    def closed(self, reason):
        stats = self.crawler.stats.get_stats()
        start_time = stats.get("start_time")
        end_time = datetime.utcnow()
        difference = end_time - start_time
        self.logger.info(f"Total scraping time: {difference} seconds")


def main(item):
    try:
        logging.info(f'Running product pages scraping for competitor: {item["competitor"]}, '
                     f'country: {item["country"]}, category: {item["category"]},'
                     f'page_number: {item["page_number"]}.')

        bucket_name = os.getenv('BUCKET_NAME', 'made-dev-competitor-analysis')
        date_string = datetime.now().strftime('%Y-%m-%d')

        key = f'{item["country"]}-{item["competitor"]}-{item["category"]}-{item["page_number"]}'

        process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'FEED_FORMAT': 'json',
            'FEED_URI': f's3://{bucket_name}/category-product-pages/{date_string}/{key}.json'
        })

        process.crawl(ProductPagesSpider, item=item)
        process.start()

        return {
            "result": "success"
        }

    except Exception as e:
        return {
            "result": "error",
            "error_message": e
        }


def handler(event, context):
    is_valid = event_validator.validate(event)

    if not is_valid:
        return {
            "result": "error",
            "error_message": f"Wrong input - {event_validator.errors}"
        }

    items = event["Records"]
    item = json.loads(items[0]["body"])

    return main(item)

