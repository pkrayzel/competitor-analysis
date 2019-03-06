import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import datetime

from common import Converter


class ProductPagesSpider(scrapy.Spider):

    name = 'product-pages'

    custom_setting = {
        "LOG_LEVEL": "INFO"
    }

    def __init__(self, items=None):
        self.items = items

        print(f"received items: {items}")

    def start_requests(self):
        for item in self.items:
            yield scrapy.Request(item["category_url"],
                                 meta={
                                     'country': item["country"],
                                     'competitor': item["competitor"],
                                     'category': item["category"]
                                 })

    def parse(self, response):
        print(response.url)
        pass

    def closed(self, reason):
        stats = self.crawler.stats.get_stats()
        start_time = stats.get("start_time")
        end_time = datetime.utcnow()
        difference = end_time - start_time
        self.logger.info(f"Total scraping time: {difference} seconds")

def handler(event, context):
    bucket_name = "made-dev-competitor-analysis"
    date_string = datetime.now().strftime('%Y%m%d%H%M')

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'FEED_FORMAT': 'json',
        'FEED_URI': f's3://{bucket_name}/category-product-pages/{date_string}.json'
    })

    items = []

    for item in event["Records"]:
        dynamodb_item = item["dynamodb"]["NewImage"]
        json_item = Converter.convert_dynamodb_item_to_json(dynamodb_item)

        print(json_item)

        items.append(json_item)

    process.crawl(ProductPagesSpider, items=items)
    process.start()

    return {
        "result": "success"
    }

if __name__ == "__main__":
    handler('', '')
