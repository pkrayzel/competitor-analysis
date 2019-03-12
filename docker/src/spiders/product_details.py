import scrapy
from scrapy.crawler import CrawlerRunner
from multiprocessing import Process, Queue
from twisted.internet import reactor


from datetime import datetime



class ProductPagesSpider(scrapy.Spider):

    name = 'product-details'

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
            deferred = runner.crawl(ProductPagesSpider, item=item)
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