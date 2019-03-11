import logging
from selenium import webdriver
from bs4 import BeautifulSoup
import time

from competitors.common import Competitor
from domain.model import ProductInformation


class BoliaCompetitor(Competitor):

    CATEGORIES_URL = {
        # "2_seat_sofas": {"url": "https://www.bolia.com/nl-nl/banken/alle-banken/?Model=2-zitsbank&Model=2%C2%BD-zitsbank&size=10000"},
        # "3_seat_sofas": {"url": "https://www.bolia.com/nl-nl/banken/alle-banken/?Category=Banken&Model=3-zitsbank&size=1000"},
        "corner_sofa": {"url": "https://www.bolia.com/nl-nl/banken/hoekbanken/?size=1000"},
        # "sofa_beds": {"url": "https://www.bolia.com/nl-nl/banken/slaapbanken/?Category=Slaapbanken&Chaise%20OE=Zonder%20chaise%20longue%20en%20open%20end&size=1000"},
        # "arm_chairs": {"url": "https://www.bolia.com/nl-nl/meubels/woonkamer/fauteuils/?Category=Fauteuils&size=1000"},
        # "dining_chairs": {"url": "https://www.bolia.com/nl-nl/meubels/eetkamer/eetkamerstoelen/?Category=Eetkamerstoelen&size=1000"},
        # "pendant_lights": {"url": "https://www.bolia.com/nl-nl/accessoires/lampen/hanglampen/?Family=Arita&Family=Ball&Family=Balloon&Family=Bell-A&Family=Bulb&Family=Cover&Family=Cyla&Family=Flachmann&Family=Glasblase&Family=Grape&Family=In%20Circles&Family=LED%20bulb&Family=Leaves&Family=Maiko&Family=Orb&Family=Pica&Family=Piper&Family=Pop&Family=Rotate&Family=Slice&Family=Squeeze&Family=Vetro"},
        # "wall_lights": {"url": "https://www.bolia.com/nl-nl/accessoires/lampen/wandlampen/?Material=Glas&Material=Marmer&Material=Staal"},
        # "floor_lights": {"url": "https://www.bolia.com/nl-nl/accessoires/lampen/vloerlampen/?Material=Acryl&Material=Glas&Material=Marmer&Material=Staal"},
        # "table_lights": {"url": "https://www.bolia.com/nl-nl/accessoires/lampen/tafellampen/?Material=Beton&Material=Glas&Material=Marmer&Material=Staal"},
    }

    def __init__(self):
        self.name = 'bolia'
        self.country = 'nl'
        self.products_per_page = 1000
        self.driver = webdriver.PhantomJS()
        super().__init__(
            name=self.name,
            country=self.country,
            products_per_page=self.products_per_page
        )

    def get_categories_urls(self):
        return self.CATEGORIES_URL

    def parse_category_details(self, response):
        # we need to render this through browser
        # because of the javascript
        self.driver.get(response.url)

        self._wait_for_element_in_driver("absolute pin cursor-pointer")

        self.loaded_content = BeautifulSoup(self.driver.page_source, 'html.parser')

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

    def _wait_for_element_in_driver(self, search_text, timeout=45, interval=1):
        interrupts = int(timeout / interval)

        for i in range(interrupts):
            logging.info(f"Waiting for page to be rendered - attempt {i}...")
            if search_text in self.driver.page_source:
                logging.info(f"Found control text {search_text} in page source...")
                return True

            logging.info(f"Haven't found control text: {search_text} - sleeping for {interval}...")
            time.sleep(interval)
        return False

    def parse_products_count(self, response):
        total_span = self.loaded_content.find("span", {"ng-bind": "$ctrl.result"})

        if total_span:
            result = total_span.get_text()
            try:
                result = int(result)
                return result
            except Exception as e:
                logging.error(f"Error while getting total products count for Bolia category {response.meta['category']}")

        return 0

    def parse_products_links_from_category_page(self, response):
        detail_links = self.loaded_content.find_all("a", class_="absolute pin cursor-pointer")
        return list(map(lambda l: f'https://www.bolia.com{l["href"]}', detail_links))

    def construct_next_page_for_category(self, category_url, page_number):
        raise NotImplementedError("Should not be needed for Bolia")

    def parse_product_price(self, response):
        raise NotImplementedError("Not implemented yet for Bolia")

    def parse_product_title(self, response):
        raise NotImplementedError("Not implemented yet for Bolia")

    def parse_technical_details(self, response):
        raise NotImplementedError("Not implemented yet for Bolia")

    def convert_to_product_information(self, product_page_item):
        raise NotImplementedError("Not implemented yet for Bolia")
