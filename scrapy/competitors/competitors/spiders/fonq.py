import scrapy
import logging

logger = logging.getLogger('fonq')


class FonqSpider(scrapy.Spider):

    name = 'fonq'
    custom_settings = {
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_START_DELAY": 1,
        "AUTOTHROTTLE_MAX_DELAY": 3,
        "DOWNLOAD_DELAY": 1,
    }

    def __init__(self, category='', **kwargs):
        start_urls = []
        try:
            file_ = f"competitors/categories/fonq/{category}.txt"
            with open(file_, 'r') as input_data:
                lines = input_data.read().splitlines()

                for l in lines:
                    if not l.startswith("#"):
                        start_urls.append(l)
        except Exception as e:
            logger.error(f"Problem reading category file with urls: {e}")

        logger.info(f"Total number of urls read from files: {len(start_urls)}")
        self.start_urls = start_urls
        super().__init__(**kwargs)

    def parse(self, response):
        products = response.css('div.product-new')

        for p in products:
            detail_link = p.css('a.link-muted::attr(href)').get()
            url = f"https://www.fonq.nl{detail_link}"

            logger.debug(f'Scraping product detail: {detail_link}')
            yield scrapy.Request(url, callback=FonqSpider.parse_product_detail)

    @staticmethod
    def parse_product_detail(response):
        title = response.css('h1::text').get()

        result = {
            'page_url': response.url,
            'title': title,
        }

        FonqSpider.parse_price(response, result)
        FonqSpider.parse_categories(response, result)
        FonqSpider.parse_technical_details(response, result)

        yield result

    @staticmethod
    def parse_price(response, result):
        try:
            price = response.css('div.price').xpath('span/text()').get()

            if price:
                # price is in format "1.123,43,-"
                price = price.replace(',-', '').replace('.-', '').replace(' ', '').replace('.', '').replace(',', '.')
                price = float(price)
                result['price'] = price
        except Exception as e:
            logging.warning(f"Exception when parsing price: {e}")

    @staticmethod
    def parse_categories(response, result):
        try:
            # category of product
            categories = response.css('ul.breadcrumb li a span::text').getall()

            for i, category in enumerate(categories):
                result[f"category_{i+1}"] = category
        except Exception as e:
            logging.warning(f"Exception when parsing categories: {e}")

    @staticmethod
    def parse_technical_details(response, result):
        try:
            # technical specification
            rows = response.xpath('//table //tr')

            for row in rows:
                # there are three different label styles (span, strong and span+strong (explanation)
                label = row.xpath('./td/span/text()').get()

                if not label or label == '\n':
                    label = row.xpath('./td/strong/text()').get()
                if not label or label == '\n':
                    label = row.xpath('./td/span/strong/text()').get()

                value = row.xpath('./td[2]/text()').get()

                if label and value:
                    label = label.replace('\n', '').replace(' ', '_').replace('/', '_').lower()
                    result[label] = value

        except Exception as e:
            logging.warning(f"Exception when parsing categories: {e}")


