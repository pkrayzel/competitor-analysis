import logging
import math


class Competitor:

    def __init__(self, name, country, products_per_page=100):
        self.name = name
        self.country = country
        self.products_per_page = products_per_page

    def get_categories_urls(self):
        raise NotImplemented("Must be implemented in child class")

    def parse_category_details(self, response):
        products_count = self.parse_products_count(response)
        return {
            'country': response.meta['country'],
            'competitor': response.meta['competitor'],
            'category': response.meta['category'],
            'products_count': products_count,
            'pages_count': self.get_pages_count(products_count),
            'category_url': response.url
        }

    def parse_products_count(self, response):
        raise NotImplemented("Must be implemented in child class")

    def get_pages_count(self, products_count):
        return math.ceil(products_count / self.products_per_page)


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
