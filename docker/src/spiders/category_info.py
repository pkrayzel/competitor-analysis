from datetime import datetime
import types
import logging

import scrapy
from scrapy.crawler import CrawlerRunner

from multiprocessing import Process, Queue
from twisted.internet import reactor

from competitors import find_competitor


class CategoryInfoSpider(scrapy.Spider):

    name = 'category-info'

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
        logging.info(
            f"Parsing first page for competitor: {response.meta['competitor']} and category: {response.meta['category']}")
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
        logging.info(f"Parsing next pages ({response.meta['page_number']}/{response.meta['pages_count']}) "
                     f"for competitor: {response.meta['competitor']} and category: {response.meta['category']}")
        competitor = find_competitor(name=response.meta['competitor'], country=response.meta['country'])
        yield competitor.parse_category_details(response)

    def closed(self, reason):
        stats = self.crawler.stats.get_stats()
        start_time = stats.get("start_time")
        end_time = datetime.utcnow()
        difference = end_time - start_time
        logging.info(f"Total scraping time: {difference} seconds")


def run_category_info(competitor):
    date_string = datetime.now().strftime('%Y-%m-%d')

    file_name = f'category-overall-info_{date_string}_{competitor["country"]}_{competitor["name"]}.json'

    def f(q):
        try:
            runner = CrawlerRunner({
                'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
                'FEED_FORMAT': 'json',
                'FEED_URI': file_name
            })
            deferred = runner.crawl(CategoryInfoSpider, competitors=[competitor])
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
