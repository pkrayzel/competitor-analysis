import scrapy
import logging

logger = logging.getLogger('fonq')


class FonqSpider(scrapy.Spider):

    name = 'fonq'

    start_urls = [
    #     # 2 seat sofas
    #     'https://www.fonq.nl/producten/categorie-2_zitsbank/',
    #     'https://www.fonq.nl/producten/categorie-2_zitsbank/?p=2',
    #     'https://www.fonq.nl/producten/categorie-2_zitsbank/?p=3',
    #     #  # 3 seat sofas
    #       "https://www.fonq.nl/producten/categorie-3_zitsbank/",
    #       "https://www.fonq.nl/producten/categorie-3_zitsbank/?p=2",
    #       "https://www.fonq.nl/producten/categorie-3_zitsbank/?p=3",
    #       "https://www.fonq.nl/producten/categorie-3_zitsbank/?p=4",
        # corner_sofa
        #   "https://www.fonq.nl/producten/categorie-hoekbank/",
        #   "https://www.fonq.nl/producten/categorie-hoekbank/?p=2"
    #     #  # sofa bed
    #     "https://www.fonq.nl/producten/categorie-slaapbanken/",
    #     "https://www.fonq.nl/producten/categorie-slaapbank/?p=2",
    #     "https://www.fonq.nl/producten/categorie-slaapbank/?p=3",
    #     "https://www.fonq.nl/producten/categorie-slaapbank/?p=4",
    #     "https://www.fonq.nl/producten/categorie-slaapbank/?p=5",
    #     "https://www.fonq.nl/producten/categorie-fauteuil/",
    #     "https://www.fonq.nl/producten/categorie-fauteuil/?p=2",
    #     "https://www.fonq.nl/producten/categorie-fauteuil/?p=3",
    #     "https://www.fonq.nl/producten/categorie-fauteuil/?p=4",
    #     "https://www.fonq.nl/producten/categorie-fauteuil/?p=5",
    #     "https://www.fonq.nl/producten/categorie-fauteuil/?p=6",
    #     "https://www.fonq.nl/producten/categorie-fauteuil/?p=7",
    #     "https://www.fonq.nl/producten/categorie-fauteuil/?p=8",
    #     "https://www.fonq.nl/producten/categorie-fauteuil/?p=9",
    #     "https://www.fonq.nl/producten/categorie-fauteuil/?p=10",
    #     "https://www.fonq.nl/producten/categorie-fauteuil/?p=11",
    #     "https://www.fonq.nl/producten/categorie-fauteuil/?p=12",
    #     "https://www.fonq.nl/producten/categorie-fauteuil/?p=13",
    #     "https://www.fonq.nl/producten/categorie-fauteuil/?p=14",
    #     "https://www.fonq.nl/producten/categorie-fauteuil/?p=15",
    #     # # "dining_chairs": {
    #     "https://www.fonq.nl/producten/categorie-eetkamerstoel/",
    #     "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=2",
    #     "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=3",
    #     "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=4",
    #     "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=5",
    #     "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=6",
    #     "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=7",
    #     "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=8",
    #     "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=9",
    #     "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=10",
        # "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=11",
        # "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=12",
        # "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=13",
        # "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=14",
        # "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=15",
        # "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=16",
        # "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=17",
        # "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=18",
        # "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=19",
        # "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=20",
        # "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=21",
        # "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=22",
        # "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=23",
        # "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=24",
        # "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=25",
        # "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=26",
        # "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=27",
        # "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=28",
        # "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=29",
        # "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=30",
        # "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=31",
        # "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=32",
        # "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=33",
        # "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=34",
        # "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=35",
        # "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=36",
        # "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=37",
        # "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=38",
        # "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=39",
        # "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=40",
        # "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=41",
        # "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=42",
        # "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=43",
        # "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=44",
        # "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=45",
        # "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=46",
    #     # # "beds"
    #     # "https://www.fonq.nl/producten/categorie-tweepersoonsbedden/?ms_fk_model=Tweepersoons&templateid=1452"
    #     # # "boxspring_beds"
    #     # "https://www.fonq.nl/producten/categorie-bedden/?ms_fk_model=Tweepersoons&templateid=1452",
    #     # "https://www.fonq.nl/producten/categorie-bedden/?ms_fk_model=Tweepersoons&p=2&templateid=1452"
    #     # # "rugs"
    #     # "https://www.fonq.nl/producten/categorie-vloerkleden/vorm-rechthoekig/",
    #     # "https://www.fonq.nl/producten/categorie-vloerkleden/?ms_fk_vorm=Rechthoekig&p=2&templateid=339",
    #     # "https://www.fonq.nl/producten/categorie-vloerkleden/?ms_fk_vorm=Rechthoekig&p=3&templateid=339",
    #     # "https://www.fonq.nl/producten/categorie-vloerkleden/?ms_fk_vorm=Rechthoekig&p=4&templateid=339",
    #     # "https://www.fonq.nl/producten/categorie-vloerkleden/?ms_fk_vorm=Rechthoekig&p=5&templateid=339",
    #     # "https://www.fonq.nl/producten/categorie-vloerkleden/?ms_fk_vorm=Rechthoekig&p=6&templateid=339",
    #     # "https://www.fonq.nl/producten/categorie-vloerkleden/?ms_fk_vorm=Rechthoekig&p=7&templateid=339",
    #     # "https://www.fonq.nl/producten/categorie-vloerkleden/?ms_fk_vorm=Rechthoekig&p=8&templateid=339",
    #     # "https://www.fonq.nl/producten/categorie-vloerkleden/?ms_fk_vorm=Rechthoekig&p=9&templateid=339",
    #     # "https://www.fonq.nl/producten/categorie-vloerkleden/?ms_fk_vorm=Rechthoekig&p=10&templateid=339",
    #     # "https://www.fonq.nl/producten/categorie-vloerkleden/?ms_fk_vorm=Rechthoekig&p=11&templateid=339",
    #     # "https://www.fonq.nl/producten/categorie-vloerkleden/?ms_fk_vorm=Rechthoekig&p=12&templateid=339",
    #     # "https://www.fonq.nl/producten/categorie-vloerkleden/?ms_fk_vorm=Rechthoekig&p=13&templateid=339",
    #     # "https://www.fonq.nl/producten/categorie-vloerkleden/?ms_fk_vorm=Rechthoekig&p=14&templateid=339",
    #     # "https://www.fonq.nl/producten/categorie-vloerkleden/?ms_fk_vorm=Rechthoekig&p=15&templateid=339",
    #     # "https://www.fonq.nl/producten/categorie-vloerkleden/?ms_fk_vorm=Rechthoekig&p=16&templateid=339",
    #     # "https://www.fonq.nl/producten/categorie-vloerkleden/?ms_fk_vorm=Rechthoekig&p=17&templateid=339",
    #     # "https://www.fonq.nl/producten/categorie-vloerkleden/?ms_fk_vorm=Rechthoekig&p=18&templateid=339",
    #     # "https://www.fonq.nl/producten/categorie-vloerkleden/?ms_fk_vorm=Rechthoekig&p=19&templateid=339",
    #     # # "pendant_lights"
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=2",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=3",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=4",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=5",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=6",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=7",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=8",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=9",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=10",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=11",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=12",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=13",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=14",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=15",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=16",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=17",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=18",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=19",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=20",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=21",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=22",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=23",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=24",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=25",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=26",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=27",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=28",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=29",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=30",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=31",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=32",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=33",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=34",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=35",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=36",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=37",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=38",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=39",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=40",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=41",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=42",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=43",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=44",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=45",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=46",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=47",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=48",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=49",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=50",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=51",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=52",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=53",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=54",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=55",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=56",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=57",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=58",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=59",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=60",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=61",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=62",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=63",
    #     # "https://www.fonq.nl/producten/categorie-hanglampen/?p=64",
    #     # # "wall_lights":
    #     # "https://www.fonq.nl/producten/categorie-wandlampen/",
    #     # "https://www.fonq.nl/producten/categorie-wandlampen/?p=2",
    #     # "https://www.fonq.nl/producten/categorie-wandlampen/?p=3",
    #     # "https://www.fonq.nl/producten/categorie-wandlampen/?p=4",
    #     # "https://www.fonq.nl/producten/categorie-wandlampen/?p=5",
    #     # "https://www.fonq.nl/producten/categorie-wandlampen/?p=6",
    #     # "https://www.fonq.nl/producten/categorie-wandlampen/?p=7",
    #     # "https://www.fonq.nl/producten/categorie-wandlampen/?p=8",
    #     # "https://www.fonq.nl/producten/categorie-wandlampen/?p=9",
    #     # "https://www.fonq.nl/producten/categorie-wandlampen/?p=10",
    #     # "https://www.fonq.nl/producten/categorie-wandlampen/?p=11",
    #     # "https://www.fonq.nl/producten/categorie-wandlampen/?p=12",
    #     # "https://www.fonq.nl/producten/categorie-wandlampen/?p=13",
    #     # "https://www.fonq.nl/producten/categorie-wandlampen/?p=14",
    #     # "https://www.fonq.nl/producten/categorie-wandlampen/?p=15",
    #     # "https://www.fonq.nl/producten/categorie-wandlampen/?p=16",
    #     # # "floor_lights": {
    #     # "https://www.fonq.nl/producten/categorie-vloerlampen/",
    #     # "https://www.fonq.nl/producten/categorie-vloerlampen/?p=2",
    #     # "https://www.fonq.nl/producten/categorie-vloerlampen/?p=3",
    #     # "https://www.fonq.nl/producten/categorie-vloerlampen/?p=4",
    #     # "https://www.fonq.nl/producten/categorie-vloerlampen/?p=5",
    #     # "https://www.fonq.nl/producten/categorie-vloerlampen/?p=6",
    #     # "https://www.fonq.nl/producten/categorie-vloerlampen/?p=7",
    #     # "https://www.fonq.nl/producten/categorie-vloerlampen/?p=8",
    #     # "https://www.fonq.nl/producten/categorie-vloerlampen/?p=9",
    #     # "https://www.fonq.nl/producten/categorie-vloerlampen/?p=10",
    #     # "https://www.fonq.nl/producten/categorie-vloerlampen/?p=11",
    #     # "https://www.fonq.nl/producten/categorie-vloerlampen/?p=12",
    #     # "https://www.fonq.nl/producten/categorie-vloerlampen/?p=13",
    #     # "https://www.fonq.nl/producten/categorie-vloerlampen/?p=14",
    #     # "https://www.fonq.nl/producten/categorie-vloerlampen/?p=15",
    #     # "https://www.fonq.nl/producten/categorie-vloerlampen/?p=16",
    #     # "https://www.fonq.nl/producten/categorie-vloerlampen/?p=17",
    #     # "https://www.fonq.nl/producten/categorie-vloerlampen/?p=18",
    #     # "https://www.fonq.nl/producten/categorie-vloerlampen/?p=19",
    #     # "https://www.fonq.nl/producten/categorie-vloerlampen/?p=20",
    #     # "https://www.fonq.nl/producten/categorie-vloerlampen/?p=21",
    #     # "https://www.fonq.nl/producten/categorie-vloerlampen/?p=22",
    #     # "https://www.fonq.nl/producten/categorie-vloerlampen/?p=23",
    #     # "https://www.fonq.nl/producten/categorie-vloerlampen/?p=24",
    #     # "https://www.fonq.nl/producten/categorie-vloerlampen/?p=25",
    #     # "https://www.fonq.nl/producten/categorie-vloerlampen/?p=26",
    #     # # "table_lights": {
    #     # "https://www.fonq.nl/producten/categorie-tafellampen/",
    #     # "https://www.fonq.nl/producten/categorie-tafellampen/?p=2",
    #     # "https://www.fonq.nl/producten/categorie-tafellampen/?p=3",
    #     # "https://www.fonq.nl/producten/categorie-tafellampen/?p=4",
    #     # "https://www.fonq.nl/producten/categorie-tafellampen/?p=5",
    #     # "https://www.fonq.nl/producten/categorie-tafellampen/?p=6",
    #     # "https://www.fonq.nl/producten/categorie-tafellampen/?p=7",
    #     # "https://www.fonq.nl/producten/categorie-tafellampen/?p=8",
    #     # "https://www.fonq.nl/producten/categorie-tafellampen/?p=9",
    #     # "https://www.fonq.nl/producten/categorie-tafellampen/?p=10",
    #     # "https://www.fonq.nl/producten/categorie-tafellampen/?p=11",
    #     # "https://www.fonq.nl/producten/categorie-tafellampen/?p=12",
    #     # "https://www.fonq.nl/producten/categorie-tafellampen/?p=13",
    #     # "https://www.fonq.nl/producten/categorie-tafellampen/?p=14",
    #     # "https://www.fonq.nl/producten/categorie-tafellampen/?p=15",
    #     # "https://www.fonq.nl/producten/categorie-tafellampen/?p=16",
    #     # "https://www.fonq.nl/producten/categorie-tafellampen/?p=17",
    #     # "https://www.fonq.nl/producten/categorie-tafellampen/?p=18",
    #     # "https://www.fonq.nl/producten/categorie-tafellampen/?p=19",
    #     # "https://www.fonq.nl/producten/categorie-tafellampen/?p=20",
    #     # "https://www.fonq.nl/producten/categorie-tafellampen/?p=21",
    #     # "https://www.fonq.nl/producten/categorie-tafellampen/?p=22",
    #     # "https://www.fonq.nl/producten/categorie-tafellampen/?p=23",
    #     # "https://www.fonq.nl/producten/categorie-tafellampen/?p=24",
    #     # "https://www.fonq.nl/producten/categorie-tafellampen/?p=25",
    #     # "https://www.fonq.nl/producten/categorie-tafellampen/?p=26",
    #     # "https://www.fonq.nl/producten/categorie-tafellampen/?p=27",
    #     # "https://www.fonq.nl/producten/categorie-tafellampen/?p=28",
    #     # "https://www.fonq.nl/producten/categorie-tafellampen/?p=29",
    ]

    def __init__(self, category_urls='', **kwargs):
        self.start_urls = category_urls.split(',')
        super().__init__(**kwargs)  # python3

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


