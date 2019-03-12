import os
import logging
import time
import json
import scrapy
from scrapy.crawler import CrawlerRunner
from multiprocessing import Process, Queue
from twisted.internet import reactor


from datetime import datetime

from competitors import find_competitor
from adapters import dao


logging.getLogger('urllib3').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('boto3').setLevel(logging.CRITICAL)


class ProductPagesSpider(scrapy.Spider):

    name = 'product-pages'

    custom_settings = {
        "DOWNLOAD_DELAY": 0,
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


def scrape_product_links(item):
    bucket_name = os.getenv('BUCKET_NAME', 'made-dev-competitor-analysis')
    date_string = datetime.now().strftime('%Y-%m-%d')

    key = f'{item["country"]}_{item["competitor"]}_{item["category"]}_{item["page_number"]}'

    logging.info(f'Will scrape product links for {key}')

    def f(q):
        try:
            runner = CrawlerRunner({
                'LOG_LEVEL': 'ERROR',
                'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
                'FEED_FORMAT': 'json',
                'FEED_URI': f's3://{bucket_name}/category-product-pages/{date_string}/{key}.json'
            })
            deferred = runner.crawl(ProductPagesSpider, item=item)
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            q.put(None)
        except Exception as e:
            q.put(e)

    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result


def consume_from_sqs():
    logging.info('Running SQS reader')

    queue_name = os.getenv('QUEUE_NAME', 'competitor-analysis-products-queue-dev')
    queue_client = dao.QueueClient(queue_name=queue_name)

    while True:
        message, receipt_handle = queue_client.receive_message()

        if message:
            item = json.loads(message)
            scrape_product_links(item)

            queue_client.delete_message(receipt_handle)
            logging.info("Consumed product links...")
        else:
            logging.info("No SQS messages found - sleeping for 30 seconds")
            time.sleep(30)


if __name__ == "__main__":
    consume_from_sqs()
