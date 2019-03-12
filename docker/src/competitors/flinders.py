import logging
from competitors.common import Competitor
from domain.model import ProductInformation
from collections import defaultdict


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

    def convert_to_product_information(self, product_page_item):
        result = ProductInformation()

        product_details = product_page_item["product_info"]
        result.price = product_details.get("price", 0.0)
        result.title = product_details.get("title", "")

        technical_details = product_details["technical_details"]

        dimensions = self._get_dimensions_from_technical_details(technical_details)

        result.width = dimensions["width"]
        result.height = dimensions["height"]
        result.depth = dimensions["depth"]
        result.diameter = dimensions["diameter"]

        result.seat_height = float(technical_details.get("zithoogte", 0.0))

        result.material = technical_details.get("materiaal", "")
        result.color = technical_details.get("kleur", "")

        return result

    def _get_dimensions_from_technical_details(self, technical_details):
        """
        "afmetingen": "(b) 190 x (d) 86 x (h) 85 cm"
        "afmetingen": "(b) 18 x (d) 38 cm"
        "afmetingen": "(b) 53.00 x (d) 6.50 x (h) 55.00 cm"
        ...
        width, depth, height = [float(s) for s in dimensions.split() if s.isdigit()]
        :param dimensions:
        :return:
        """
        result = defaultdict(lambda: 0.0)

        dimensions = technical_details.get("afmetingen")
        if not dimensions:
            return result

        # "(b) 190 x (d) 86 x (h) 85 cm" -> "(b)190x(d)86x(h)85"
        # "(b) 18 x (d) 38 cm" -> "(b)18x(d)38"
        # "(b) 53.00 x (d) 6.50 x (h) 55.00 cm" -> "(b)53.00x(d)6.50x(h)55.00"
        dimensions = dimensions.replace('cm', '').replace(' ', '')

        # "(b)190x(d)86x(h)85" -> ["(b)190", "(d)86", "(h)85"]
        # "(b)18x(d)38" -> ["(b)18", "(d)38"]
        # "(b)53.00x(d)6.50x(h)55.00" -> ["(b)53.00", "(d)6.50", "(h)55.00"]
        values = dimensions.split('x')

        for v in values:

            if v.startswith("(d)"):
                result["depth"] = self._convert_value_to_float_safely(v.replace('(d)', ''))
            elif v.startswith("(b)"):
                result["width"] = self._convert_value_to_float_safely(v.replace('(b)', ''))
            elif v.startswith("(h)"):
                result["height"] = self._convert_value_to_float_safely(v.replace('(h)', ''))
            elif v.startswith("(Ø)"):
                result["diameter"] = self._convert_value_to_float_safely(v.replace('(Ø)', ''))
            elif v.startswith("(l)"):
                result["length"] = self._convert_value_to_float_safely(v.replace('(l)', ''))
            else:
                logging.warning(f"Unexpected item received: {technical_details} - value {v}")

        return result

    def _convert_value_to_float_safely(self, text):
        try:
            return float(text)
        except Exception as e:
            logging.warning(f"Can't convert text to float - {text}")
        return 0.0