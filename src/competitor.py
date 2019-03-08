import logging
import math


class Competitor:

    def __init__(self, name, country, products_per_page=100):
        self.name = name
        self.country = country
        self.products_per_page = products_per_page

    def parse_category_details(self, response):
        products_count = self.parse_products_count(response)
        product_links = self.parse_products_links_from_category_page(response)
        return {
            'country': response.meta['country'],
            'competitor': response.meta['competitor'],
            'category': response.meta['category'],
            'category_url': response.meta['category_url'],
            'page_url': response.url,
            'pages_count': self.get_pages_count(products_count),
            'page_number': response.meta['page_number'],
            'products_count': products_count,
            'product_links_count': len(product_links),
            'product_links': product_links
        }

    def get_next_pages_for_category(self, category_details):
        result = []

        for i in range(2, category_details["pages_count"] + 1):

            url = self.construct_next_page_for_category(category_details["category_url"], i)
            meta = {
                'country': category_details["country"],
                'competitor': category_details["competitor"],
                'category': category_details["category"],
                'category_url': category_details["category_url"],
                'page_number': i
            }
            result.append((url, meta))

        return result

    def parse_products_links(self, response):
        links = self.parse_products_links_from_category_page(response)

        return {
            'country': response.meta['country'],
            'competitor': response.meta['competitor'],
            'category': response.meta['category'],
            'products_count': response.meta['products_count'],
            'page_number': response.meta['page_number'],
            'links_count': len(links),
            'pages_count': response.meta['pages_count'],
            'product_links': links
        }

    def parse_product_detail(self, response):
        price = self.parse_product_price(response)
        title = self.parse_product_title(response)
        technical_details = self.parse_technical_details(response)

        return {
            'country': response.meta['country'],
            'competitor': response.meta['competitor'],
            'category': response.meta['category'],
            'category_url': response.meta['category_url'],
            'page_url': response.url,
            'product_number': response.meta['product_number'],
            'page_number': response.meta['page_number'],
            'product_info': {
                'price': float(price),
                'title': title,
                'technical_details': technical_details
            }
        }

    def get_pages_count(self, products_count):
        return math.ceil(products_count / self.products_per_page)

    # following methods must be implemented by each competitor subclass
    def parse_products_count(self, response):
        raise NotImplemented("Must be implemented in child class")

    def get_categories_urls(self):
        raise NotImplemented("Must be implemented in child class")

    def construct_next_page_for_category(self, category_url, page_number):
        raise NotImplementedError("Must be implemented in child class")

    def parse_products_links_from_category_page(self, response):
        raise NotImplemented("Must be implemented in child class")

    def parse_product_price(self, response):
        raise NotImplemented("Must be implemented in child class")

    def parse_product_title(self, response):
        raise NotImplemented("Must be implemented in child class")

    def parse_technical_details(self, response):
        raise NotImplemented("Must be implemented in child class")


class FonqCompetitor(Competitor):

    CATEGORIES_URL = {
        "2_seat_sofas": {"url": "https://www.fonq.nl/producten/categorie-2_zitsbank/"},
        "3_seat_sofas": {"url": "https://www.fonq.nl/producten/categorie-3_zitsbank/"},
        "corner_sofa": {"url": "https://www.fonq.nl/producten/categorie-hoekbank/"},
        "sofa_beds": {"url": "https://www.fonq.nl/producten/categorie-slaapbanken/"},
        "arm_chairs": {"url": "https://www.fonq.nl/producten/categorie-fauteuil/"},
        "dining_chairs": {"url": "https://www.fonq.nl/producten/categorie-eetkamerstoel/"},
        "beds": {
            "url": "https://www.fonq.nl/producten/categorie-tweepersoonsbedden/?ms_fk_model=Tweepersoons&templateid=1452"},
        "boxspring_beds": {
            "url": "https://www.fonq.nl/producten/categorie-bedden/?ms_fk_model=Tweepersoons&templateid=1452"},
        "rugs": {"url": "https://www.fonq.nl/producten/categorie-vloerkleden/vorm-rechthoekig/"},
        "pendant_lights": {"url": "https://www.fonq.nl/producten/categorie-hanglampen/"},
        "wall_lights": {"url": "https://www.fonq.nl/producten/categorie-wandlampen/"},
        "floor_lights": {"url": "https://www.fonq.nl/producten/categorie-vloerlampen/"},
        "table_lights": {"url": "https://www.fonq.nl/producten/categorie-tafellampen/"},
    }

    def __init__(self):
        self.name = 'fonq'
        self.country = 'nl'
        self.products_per_page = 48
        super().__init__(
            name=self.name,
            country=self.country,
            products_per_page=self.products_per_page
        )

    def get_categories_urls(self):
        return self.CATEGORIES_URL

    def parse_products_count(self, response):
        try:
            counts_link = response.css('li.facet-summary__links-count span strong::text').getall()[-1]
            return int(counts_link)
        except Exception as e:
            logging.warning(f"Exception when parsing total count: {e}")
        return 0

    def parse_products_links_from_category_page(self, response):
        links = response.css('div.product-body').xpath('a[1]//@href').extract()
        return list(map(lambda l: f"https://www.fonq.nl{l}", links))

    def construct_next_page_for_category(self, category_url, page_number):
        return f'{category_url}?p={page_number}'

    def parse_product_price(self, response):
        try:
            price = response.css('div.price').xpath('span/text()').get()
            if price:
                # price is in format "1.123,43,-"
                price = price.replace(',-', '').replace('.-', '').replace(' ', '').replace('.', '').replace(',', '.')
                price = float(price)
            else:
                price = 0
        except Exception as e:
            logging.warning(f"Fonq - exception when parsing price: {e}")

        return price

    def parse_product_title(self, response):
        title = ""
        try:
            title = response.css('li.active ::text').get()
        except Exception as e:
            logging.warning(f"Fonq - exception when parsing title: {e}")
        return title

    def parse_technical_details(self, response):
        result = {}

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
            logging.warning(f"Fonq - exception when parsing tech. details: {e}")

        return result


class FlindersCompetitor(Competitor):

    PRODUCTS_PER_PAGE = 100

    CATEGORIES_URL = {
        "2_seat_sofas": {"url": "https://www.flinders.nl/wonen-banken-2-5-zitsbanken" },
        "3_seat_sofas": {"url": "https://www.flinders.nl/wonen-banken-3-zitsbanken" },
        "corner_sofa": {"url": "https://www.flinders.nl/wonen-stoelen-fauteuils" },
        "dining_chairs": {"url": "https://www.flinders.nl/wonen-stoelen-eetkamerstoelen" },
        "beds": { "url": "https://www.flinders.nl/wonen-slaapkamer-tweepersoonsbedden"},
        "rugs": {"url": "https://www.flinders.nl/wonen-woonaccessoires-vloerkleden" },
        "pendant_lights": {"url": "https://www.flinders.nl/wonen-hanglampen" },
        "wall_lights": {"url": "https://www.flinders.nl/wonen-wandlampen" },
        "floor_lights": {"url": "https://www.flinders.nl/wonen-vloerlampen" },
        "table_lights": {"url": "https://www.flinders.nl/wonen-tafellampen" },
    }

    def __init__(self):
        self.name = 'flinders'
        self.country = 'nl'
        self.products_per_page = 100
        super().__init__(
            name=self.name,
            country=self.country,
            products_per_page=self.products_per_page
        )

    def get_categories_urls(self):
        return self.CATEGORIES_URL

    def parse_products_count(self, response):
        try:
            counts_link = response.css('span.list_count_max::text').get()
            return int(counts_link)
        except Exception as e:
            logging.warning(f"Exception when parsing total count: {e}")
        return 0

    def parse_products_links_from_category_page(self, response):
        return response.css('div.item-container').xpath('a//@href').extract()

    def construct_next_page_for_category(self, category_url, page_number):
        return f'{category_url}?p={page_number}'

    def parse_product_price(self, response):
        try:
            price = response.css('span.price ::text').get()
            if price:
                # price is in format "1.123,43,-"
                price = price.replace('€', '').replace('\xa0', '').replace('.', '').replace(',', '.')
                price = float(price)
            else:
                price = 0
        except Exception as e:
            logging.warning(f"Exception when parsing price: {e}")
        return price

    def parse_product_title(self, response):
        title = ""
        try:
            brand_name = response.css('h1::text').get()
            if brand_name:
                brand_name = brand_name.strip().replace('\r', '').replace('\n', '')

            detail_title = response.css('h1 span::text').get()
            title = f"{brand_name} {detail_title}"
        except Exception as e:
            logging.warning(f"Flinders - exception when parsing title: {e}")
        return title

    def parse_technical_details(self, response):
        result = {}
        try:
            # technical specification
            rows = response.xpath('//section[@id="content-specs"] //table //tr')

            for row in rows:
                # there are three different label styles (span, strong and span+strong (explanation)
                label = row.xpath('th//text()').get()

                if not label or label == '\n':
                    logging.error(f"Label is missing for product: {response.url}")

                value = row.xpath('td//text()').get()

                if label and value:
                    label = label.replace('\n', '').replace(' ', '_').replace('/', '_').lower()
                    result[label] = value

        except Exception as e:
            logging.warning(f"Flinders - exception when parsing tech. specification: {e}")

        return result


COMPETITORS = [
    FonqCompetitor(),
    FlindersCompetitor()
]


def find_competitor(name, country):
    for c in COMPETITORS:
        if c.name == name and c.country == country:
            return c
