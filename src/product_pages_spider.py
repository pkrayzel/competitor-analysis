from uuid import uuid4
import os
import logging
import aws_lambda_logging
import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import datetime

from converter import Converter
from competitor import find_competitor

aws_lambda_logging.setup(level='INFO', boto_level='CRITICAL')
logging.getLogger('urllib3').setLevel(logging.CRITICAL)


class ProductPagesSpider(scrapy.Spider):

    name = 'product-pages'

    custom_settings = {
        "DOWNLOAD_DELAY": 2,
        "RETRY_TIMES": 5,
        "RETRY_HTTP_CODES": [500, 502, 503, 504, 400, 403, 404, 408]
    }

    def __init__(self, item=None):
        self.item = item

    def start_requests(self):
        # in case there's more dynamodb records
        # for each product link
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


def scrape_products(items):
    try:
        bucket_name = os.getenv('BUCKET_NAME', 'made-dev-competitor-analysis')
        date_string = datetime.now().strftime('%Y%m%d')

        process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'FEED_FORMAT': 'jl',
            'FEED_URI': f's3://{bucket_name}/category-product-pages/{date_string}/{str(uuid4())}.jl'
        })

        dynamodb_item = items[0]["dynamodb"]["NewImage"]
        json_item = Converter.convert_dynamodb_item_to_json(dynamodb_item)

        process.crawl(ProductPagesSpider, item=json_item)
        process.start()

    except Exception as e:
        raise Exception(f"{str(type(e).__name__)}: {str(e)}")


def handler(event, context):
    if "Records" not in event:
        logging.error("Wrong input event - expecting 'Records' with DynamoDB stream event.")
        return { "result": "error", "message": "wrong input data" }

    items = event["Records"]

    if len(items) > 1:
        logging.error("Too many records in input event - expecting just one record.")
        return {"result": "error", "message": "wrong input data - too many records"}

    logging.info(f"Incoming event: {event}")

    scrape_products(items)

    return {
        "result": "success"
    }

if __name__ == "__main__":
    handler('', '')
