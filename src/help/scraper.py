# https://stackoverflow.com/questions/41495052/scrapy-reactor-not-restartable
import scrapy
import scrapy.crawler as crawler
from multiprocessing import Process, Pipe
from twisted.internet import reactor

# your spider
class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ['http://quotes.toscrape.com/tag/humor/']

    def parse(self, response):
        for quote in response.css('div.quote'):
            print(quote.css('span.text::text').extract_first())


def scraping(spider, conn):
    try:
        runner = crawler.CrawlerRunner()
        deferred = runner.crawl(spider)
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run()
    except Exception as e:
        print(f"Error: {e}")

    conn.send(["finished"])
    conn.close()


# the wrapper to make it run more times
def run_spider(spider):

    # create a pipe for communication
    parent_conn, child_conn = Pipe()

    # create the process, pass instance and connection
    process = Process(target=scraping, args=(spider, child_conn,))

    process.start()
    process.join()

    return parent_conn.recv()[0]


def handler(event, context):
    print("First time")
    run_spider(QuotesSpider())
    print("Second time")
    run_spider(QuotesSpider())
    print("Third time")
    run_spider(QuotesSpider())


if __name__ == "__main__":
    handler("", "")
