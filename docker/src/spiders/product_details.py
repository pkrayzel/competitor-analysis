import scrapy
from scrapy.crawler import CrawlerRunner
from multiprocessing import Process, Queue
from twisted.internet import reactor

from datetime import datetime
import logging

from competitors import find_competitor


class ProductDetailsSpider(scrapy.Spider):

    name = 'product-details'

    def __init__(self, item=None):
        self.item = item

        competitor = find_competitor(name=self.item['competitor'],
                                     country=self.item['country'])

        self.custom_settings = competitor.get_custom_settings()

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
                                     'page_products_count': len(self.item["product_links"]),
                                     'product_number': i,
                                 })

    def parse(self, response):
        logging.info(f"Parsing product details for competitor: {response.meta['competitor']}, "
                     f"country: {response.meta['country']}, "
                     f"page number: {response.meta['page_number']} "
                     f"and product number: {response.meta['product_number']}"
                     f"/{response.meta['page_products_count']}")
        competitor = find_competitor(name=response.meta['competitor'], country=response.meta['country'])
        yield competitor.parse_product_detail(response)

    def closed(self, reason):
        stats = self.crawler.stats.get_stats()
        start_time = stats.get("start_time")
        end_time = datetime.utcnow()
        difference = end_time - start_time
        self.logger.info(f"Total scraping time: {difference} seconds")


def run_product_details(item):
    date_string = datetime.now().strftime('%Y-%m-%d')

    key = f'{item["country"]}_{item["competitor"]}_{item["category"]}_{item["page_number"]}'
    file_name = f"category-product-pages_{date_string}_{key}.json"

    def f(q):
        try:
            runner = CrawlerRunner({
                'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
                'FEED_FORMAT': 'json',
                'FEED_URI': file_name
            })
            deferred = runner.crawl(ProductDetailsSpider, item=item)
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            q.put(None)
        except Exception as e:
            q.put(e)

    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    q.get()
    p.join()

    return file_name