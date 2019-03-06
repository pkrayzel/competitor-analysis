import logging
import math
import time
from datetime import datetime


class Competitor:

    def __init__(self, name, country, products_per_page=100):
        self.name = name
        self.country = country
        self.products_per_page = products_per_page

    def get_categories_urls(self):
        raise NotImplemented("Must be implemented in child class")

    def parse_category_details(self, response):
        products_count = self.parse_products_count(response)
        links = self.parse_products_links_from_category_page(response)
        return {
            'country': response.meta['country'],
            'competitor': response.meta['competitor'],
            'category': response.meta['category'],
            'category_url': response.meta['category_url'],
            'products_count': products_count,
            'pages_count': self.get_pages_count(products_count),
            'page_url': response.url,
            'page_number': response.meta['page_number'],
            'links_count': len(links),
            'product_links': links
        }

    def parse_products_count(self, response):
        raise NotImplemented("Must be implemented in child class")

    def get_pages_count(self, products_count):
        return math.ceil(products_count / self.products_per_page)

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

    def parse_products_links_from_category_page(self, response):
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


class Converter:

    def __init__(self, table_name):
        self.table_name = table_name

    @staticmethod
    def convert_dynamodb_item_to_json(item):
        result = {}
        for key, value in item.items():
            for v in value.values():
                result[key] = v
        return result

    def convert_json_items_to_put_requests(self, items):
        result = []
        for item in items:
            result.append(self.convert_json_item_to_put_request(item))
        return result

    def convert_json_item_to_put_request(self, item):
        dynamodb_item = {
            self.key_attribute_name(): Converter.convert_value(self.key_attribute_value(item)),
        }

        self.append_date_time_fields(dynamodb_item)

        for key, value in item.items():
            dynamodb_item[key] = Converter.convert_value(value)

        return {
            "PutRequest": {
                "Item": dynamodb_item
            }
        }

    def key_attribute_name(self):
        raise NotImplementedError("Must be implemented in subclasses.")

    def key_attribute_value(self, item):
        raise NotImplementedError("Must be implemented in subclasses.")

    def append_date_time_fields(self, dynamodb_item):
        date = datetime.utcnow()
        dynamodb_item["timestamp"] = Converter.convert_value(str(int(time.mktime(date.timetuple())) * 1000))
        dynamodb_item["date"] = Converter.convert_value(date.strftime("%Y-%m-%d"))
        dynamodb_item["time"] = Converter.convert_value(date.strftime("%H-%M-%S"))

    @staticmethod
    def convert_value(value):
        data_type = "S"

        if type(value) == int:
            data_type = "N"

        return {
            data_type: str(value)
        }


class ConverterOverall(Converter):

    def key_attribute_name(self):
        return "country_competitor_category"

    def key_attribute_value(self, item):
        return f"{item['country']}_{item['competitor']}_{item['category']}"


COMPETITORS = [
    FonqCompetitor(),
    FlindersCompetitor()
]


def find_competitor(name):
    for c in COMPETITORS:
        if c.name == name:
            return c
