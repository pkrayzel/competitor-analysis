import logging

from bs4 import BeautifulSoup
import time

from competitors.common import Competitor
from domain.model import ProductInformation


class BoliaCompetitor(Competitor):

    CATEGORIES_URL = {
        "2_seat_sofas": {"url": "https://www.bolia.com/nl-nl/banken/alle-banken/?Model=2-zitsbank&Model=2%C2%BD-zitsbank&size=10000"},
        "3_seat_sofas": {"url": "https://www.bolia.com/nl-nl/banken/alle-banken/?Category=Banken&Model=3-zitsbank&size=1000"},
        "corner_sofa": {"url": "https://www.bolia.com/nl-nl/banken/hoekbanken/?size=1000"},
        "sofa_beds": {"url": "https://www.bolia.com/nl-nl/banken/slaapbanken/?Category=Slaapbanken&Chaise%20OE=Zonder%20chaise%20longue%20en%20open%20end&size=1000"},
        "arm_chairs": {"url": "https://www.bolia.com/nl-nl/meubels/woonkamer/fauteuils/?Category=Fauteuils&size=1000"},
        "dining_chairs": {"url": "https://www.bolia.com/nl-nl/meubels/eetkamer/eetkamerstoelen/?Category=Eetkamerstoelen&size=1000"},
        "pendant_lights": {"url": "https://www.bolia.com/nl-nl/accessoires/lampen/hanglampen/?Family=Arita&Family=Ball&Family=Balloon&Family=Bell-A&Family=Bulb&Family=Cover&Family=Cyla&Family=Flachmann&Family=Glasblase&Family=Grape&Family=In%20Circles&Family=LED%20bulb&Family=Leaves&Family=Maiko&Family=Orb&Family=Pica&Family=Piper&Family=Pop&Family=Rotate&Family=Slice&Family=Squeeze&Family=Vetro"},
        "wall_lights": {"url": "https://www.bolia.com/nl-nl/accessoires/lampen/wandlampen/?Material=Glas&Material=Marmer&Material=Staal"},
        "floor_lights": {"url": "https://www.bolia.com/nl-nl/accessoires/lampen/vloerlampen/?Material=Acryl&Material=Glas&Material=Marmer&Material=Staal"},
        "table_lights": {"url": "https://www.bolia.com/nl-nl/accessoires/lampen/tafellampen/?Material=Beton&Material=Glas&Material=Marmer&Material=Staal"},
    }

    def __init__(self, web_client):
        self.name = 'bolia'
        self.country = 'nl'
        self.products_per_page = 50

        self.web_client = web_client

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
        self.web_client.render_url(response.url)

        logging.info(f"Parsing category details for category: {response.meta['category']}")

        self._wait_for_element_in_web_client("absolute pin cursor-pointer")

        self.loaded_content = BeautifulSoup(self.web_client.get_rendered_content(), 'html.parser')

        products_count = self.parse_products_count(response)
        product_links = self.parse_products_links_from_category_page(response)

        pages_count = self.get_pages_count(products_count)

        logging.info(f"There should be {products_count} product for category: {response.meta['category']} "
                     f"- found {len(product_links)} product links.")

        # bolia doesn't have pagination
        # but we want to split it to multiple
        # pages anyway - 50 should be a good number
        for i in range(1, pages_count + 1):
            start = (i - 1) * self.products_per_page
            end = i * self.products_per_page
            product_links_subset = product_links[start:end]
            yield {
                'country': response.meta['country'],
                'competitor': response.meta['competitor'],
                'category': response.meta['category'],
                'category_url': response.meta['category_url'],
                'page_url': response.url,
                'pages_count': pages_count,
                'page_number': i,
                'products_count': products_count,
                'product_links_count': len(product_links_subset),
                'product_links': product_links_subset
            }

    def _wait_for_element_in_web_client(self, search_text, timeout=45, interval=1):
        interrupts = int(timeout / interval)

        for i in range(interrupts):
            logging.info(f"Waiting for page to be rendered - attempt {i}...")
            if search_text in self.web_client.get_rendered_content():
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

    def get_next_pages_for_category(self, category_details):
        return []

    def construct_next_page_for_category(self, category_url, page_number):
        raise NotImplementedError("Should not be needed for Bolia")

    def parse_product_detail(self, response):
        # we need to render this through browser
        # because of the javascript
        logging.info(f"Parsing product detail for category: {response.meta['category']} and product num: {response.meta['product_number']}")

        self.web_client.render_url(response.url)
        self.loaded_content = BeautifulSoup(self.web_client.get_rendered_content(), 'html.parser')

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

    def parse_product_price(self, response):
        try:
            price = self.loaded_content.find("meta", {"property": "product:price:amount"})["content"]
            price = float(price)
            return price
        except Exception as e:
            logging.error(f"Exception parsing price for Bolia  - {e}")

    def parse_product_title(self, response):
        result = ""
        try:
            result = self.loaded_content.find("meta", {"property": "og:title"})["content"]
        except Exception as e:
            logging.error(f"Exception parsing price for Bolia  - {e}")

        return result

    def _parse_description(self):
        try:
            return self.loaded_content.find("meta", {"property": "og:description"})["content"]
        except Exception as e:
            logging.error(f"Exception parsing description for Bolia  - {e}")
        return ""

    def parse_technical_details(self, response):
        result = dict(description=self._parse_description())

        try:
            data_labels = self.loaded_content.find_all("dt", {"ng-bind": "spec.title"})
            data_values = self.loaded_content.find_all("dd", {"ng-bind": "spec.desc"})

            info_labels = self.loaded_content.find_all('dt', {"ng-bind": "info.key || info.Key"})
            info_values = self.loaded_content.find_all('dd', {"ng-bind": "info.value || info.Value"})

            data_labels.extend(info_labels)
            data_values.extend(info_values)

            for i in range(len(data_labels)):
                label = data_labels[i].get_text().lower()
                value = data_values[i].get_text()
                result[label] = value

        except Exception as e:
            logging.error(f"Exception parsing specification for Bolia - {e}")

        return result

    def convert_to_product_information(self, product_page_item):
        result = ProductInformation()

        product_details = product_page_item["product_info"]
        result.price = product_details.get("price", 0.0)
        result.title = product_details.get("title", "")

        technical_details = product_details["technical_details"]

        result.width = self._get_dimension_field_multiple(technical_details, "breedte")
        result.height = self._get_dimension_field_multiple(technical_details, "hoogte")
        result.depth = self._get_dimension_field_multiple(technical_details, "diepte")

        result.seat_height = self._get_dimension_field_multiple(technical_details, "zithoogte")

        result.material = technical_details.get("materiaal", "")
        result.color = technical_details.get("kleur", "")

        return result

    def _get_dimension_field_multiple(self, technical_details, label):
        value = technical_details.get(label, "0.0/0.00  cm")
        value = value.replace('cm', '').replace(' ', '').replace(',', '.')

        if "/" in value:
            value = value.split('/')[0]
            value = value.replace(',', '.')

        return float(value)