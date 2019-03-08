import logging
from competitors.common import Competitor


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

