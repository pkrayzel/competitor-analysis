import json
import os
import logging
import scrapy
from scrapy.crawler import CrawlerProcess
import types

from datetime import datetime

from competitors import find_competitor
from adapters import dao


FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)
logging.getLogger('scrapy').setLevel(logging.CRITICAL)



class CategorySpider(scrapy.Spider):

    name = 'category'

    def __init__(self, competitors):
        self.competitors = competitors

    def start_requests(self):
        for c in self.competitors:
            competitor = find_competitor(name=c["name"], country=c["country"])
            logging.info(f"Will scrape competitor: {competitor.name}")

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
        logging.info(f"Parsing first page for competitor: {response.meta['competitor']}")
        competitor = find_competitor(name=response.meta['competitor'], country=response.meta['country'])
        category_details = competitor.parse_category_details(response)

        # for some competitors we might return multiple pages from the first page
        # - no pagination from them, so we made that happen on purpose
        if isinstance(category_details, types.GeneratorType):
            for item in category_details:
                yield item
        # otherwise just yield the first page result
        else:
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
        logging.info(f"Total scraping time: {difference} seconds")


def run_category_spider(competitor):
    bucket_name = os.getenv('BUCKET_NAME', 'made-dev-competitor-analysis')

    date_string = datetime.now().strftime('%Y-%m-%d')

    competitor_key = f'{competitor["country"]}_{competitor["name"]}'
    s3_file_key = f"category-overall-info/{date_string}/{competitor_key}.json"

    process = CrawlerProcess({
        "LOG_LEVEL": "INFO",
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'FEED_FORMAT': 'json',
        'FEED_URI': f's3://{bucket_name}/{s3_file_key}'
    })

    process.crawl(CategorySpider, competitors=[competitor])
    process.start()

    # bucket name, file key
    return bucket_name, s3_file_key


def parse_json_to_sqs(bucket_name, s3_file_key):
    logging.info(f"Will parse json file and store it in SQS - bucket: {bucket_name}, file key: {s3_file_key}")
    queue_name = os.getenv('QUEUE_NAME', 'competitor-analysis-products-queue-dev')

    file_client = dao.FileStorageClient()
    queue_client = dao.QueueClient(queue_name=queue_name)

    file_content = file_client.get(
        bucket_name=bucket_name,
        file_key=s3_file_key
    )

    data = json.load(file_content)

    queue_client.store_items(items=data)


if __name__ == "__main__":
    # bucket_name, s3_file_key = run_category_spider({"country": "nl", "name": "flinders"})
    bucket_name, s3_file_key = run_category_spider({"country": "nl", "name": "bolia"})

    parse_json_to_sqs(bucket_name, s3_file_key)
