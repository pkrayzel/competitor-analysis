import json
import os
import logging
import aws_lambda_logging

import scrapy
from scrapy.crawler import CrawlerRunner
from multiprocessing import Process, Pipe
from twisted.internet import reactor


from datetime import datetime

from competitors import find_competitor
from validators import product_pages_validator


aws_lambda_logging.setup(level='INFO', boto_level='CRITICAL')
logging.getLogger('urllib3').setLevel(logging.CRITICAL)


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
        competitor = find_competitor(name=response.meta['competitor'], country=response.meta['country'])
        yield competitor.parse_product_detail(response)

    def closed(self, reason):
        stats = self.crawler.stats.get_stats()
        start_time = stats.get("start_time")
        end_time = datetime.utcnow()
        difference = end_time - start_time
        self.logger.info(f"Total scraping time: {difference} seconds")


def scrape_product_links(item, conn):
    error = None
    try:
        logging.info(f'Running product pages scraping for competitor: {item["competitor"]}, '
                     f'country: {item["country"]}, category: {item["category"]},'
                     f'page_number: {item["page_number"]}.')

        bucket_name = os.getenv('BUCKET_NAME', 'made-dev-competitor-analysis')
        date_string = datetime.now().strftime('%Y-%m-%d')

        key = f'{item["country"]}_{item["competitor"]}_{item["category"]}_{item["page_number"]}'

        runner = CrawlerRunner({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'FEED_FORMAT': 'json',
            'FEED_URI': f's3://{bucket_name}/category-product-pages/{date_string}/{key}.json'
        })

        deferred = runner.crawl(ProductPagesSpider, item=item)
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run()

    except Exception as e:
        logging.error(f"Error {e}")
        error = e

    conn.send([error])
    conn.close()


def main(item):
    # create a pipe for communication
    parent_conn, child_conn = Pipe()

    # create the process, pass instance and connection
    process = Process(target=scrape_product_links, args=(item, child_conn,))

    process.start()
    process.join()

    error = parent_conn.recv()[0]

    if error:
        return {
            "result": "error",
            "error_message": error
        }

    return {
            "result": "success"
    }


def handler(event, context):
    is_valid = product_pages_validator.validate(event)

    if not is_valid:
        return {
            "result": "error",
            "error_message": f"Wrong input - {product_pages_validator.errors}"
        }

    items = event["Records"]
    item = json.loads(items[0]["body"])

    return main(item)
