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
        competitor = find_competitor(response.meta['competitor'])
        category_details = competitor.parse_category_details(response)
        # yield the first page result
        yield category_details

        for i in range(1, category_details["pages_count"]):
            url = f"{response.url}?p={i}"
            yield scrapy.Request(url=url,
                                 meta={
                                     'country': category_details["country"],
                                     'competitor': category_details["competitor"],
                                     'category': category_details["category"],
                                     'category_url': category_details["category_url"],
                                     'page_number': i,
                                 },
                                 callback=self.parse_next_pages)

    def parse_next_pages(self, response):
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
