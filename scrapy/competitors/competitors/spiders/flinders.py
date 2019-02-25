import scrapy
import logging

logger = logging.getLogger('fonq')


class FlindersSpider(scrapy.Spider):

    name = 'flinders'

    start_urls = [
        "https://www.flinders.nl/wonen-banken-2-5-zitsbanken",
    ]
        # "2_seat_sofas"

        # # "3_seat_sofas"
        # "https://www.flinders.nl/wonen-banken-3-zitsbanken",
        # # "corner_sofa"
        # "https://www.flinders.nl/wonen-banken-hoekbanken",
        # "https://www.flinders.nl/wonen-stoelen-fauteuils",
        # # "dining_chairs"
        # "https://www.flinders.nl/wonen-stoelen-eetkamerstoelen",
        # "https://www.flinders.nl/wonen-stoelen-eetkamerstoelen?p=2",
        # "https://www.flinders.nl/wonen-stoelen-eetkamerstoelen?p=3",
        # "https://www.flinders.nl/wonen-stoelen-eetkamerstoelen?p=4",
        # "https://www.flinders.nl/wonen-stoelen-eetkamerstoelen?p=5",
        # # "beds"
        # "https://www.flinders.nl/wonen-slaapkamer-tweepersoonsbedden",
        # "https://www.flinders.nl/wonen-stoelen-fauteuils?p=2",
        # "https://www.flinders.nl/wonen-stoelen-fauteuils?p=3",
        # # "rugs"
        # "https://www.flinders.nl/wonen-woonaccessoires-vloerkleden",
        # "https://www.flinders.nl/wonen-woonaccessoires-vloerkleden?p=2",
        # "https://www.flinders.nl/wonen-woonaccessoires-vloerkleden?p=3",
        # "https://www.flinders.nl/wonen-woonaccessoires-vloerkleden?p=4",
        # "https://www.flinders.nl/wonen-woonaccessoires-vloerkleden?p=5",
        # # "pendant_lights"
        # "https://www.flinders.nl/wonen-hanglampen",
        # "https://www.flinders.nl/wonen-hanglampen?p=2",
        # "https://www.flinders.nl/wonen-hanglampen?p=3",
        # "https://www.flinders.nl/wonen-hanglampen?p=4",
        # "https://www.flinders.nl/wonen-hanglampen?p=5",
        # # "wall_lights"
        # "https://www.flinders.nl/wonen-wandlampen",
        # "https://www.flinders.nl/wonen-wandlampen?p=2",
        # "https://www.flinders.nl/wonen-wandlampen?p=3",
        # "https://www.flinders.nl/wonen-wandlampen?p=4",
        # "https://www.flinders.nl/wonen-wandlampen?p=5",
        # # "floor_lights"
        # "https://www.flinders.nl/wonen-vloerlampen",
        # "https://www.flinders.nl/wonen-vloerlampen?p=2",
        # "https://www.flinders.nl/wonen-vloerlampen?p=3",
        # "https://www.flinders.nl/wonen-vloerlampen?p=4",
        # "https://www.flinders.nl/wonen-vloerlampen?p=5",
        # # "table_lights"
        # "https://www.flinders.nl/wonen-tafellampen",
        # "https://www.flinders.nl/wonen-tafellampen?p=2",
        # "https://www.flinders.nl/wonen-tafellampen?p=3",
        # "https://www.flinders.nl/wonen-tafellampen?p=4",
        # "https://www.flinders.nl/wonen-tafellampen?p=5",
    # ]

    def __init__(self, category_url='', **kwargs):
        # self.start_urls = [category_url]
        super().__init__(**kwargs)  # python3

    def parse(self, response):
        products = response.css('div.item-container')

        for p in products:
            detail_link = p.css('a::attr(href)').get()

            logger.debug(f'Scraping product detail: {detail_link}')
            yield scrapy.Request(detail_link, callback=FlindersSpider.parse_product_detail)

    @staticmethod
    def parse_product_detail(response):
        brand_name = response.css('h1.branded-name::text')

        result = {
            'page_url': response.url
        }

        FlindersSpider.parse_title(response, result)
        FlindersSpider.parse_price(response, result)
        FlindersSpider.parse_categories(response, result)
        # FlindersSpider.parse_technical_details(response, result)

        yield result

    @staticmethod
    def parse_title(response, result):
        try:
            brand_name = response.css('h1::text').get()

            if brand_name:
                brand_name = brand_name.strip().replace('\r', '').replace('\n', '')
            detail_title = response.css('h1 span::text').get()
            result['title'] = brand_name + " " + detail_title

        except Exception as e:
            logging.warning(f"Exception when parsing title: {e}")

    @staticmethod
    def parse_price(response, result):
        try:
            price = response.css('span.price').get()

            if price:
                # price is in format "1.123,43,-"
                price = price.replace('€ ', '').replace('.', '').replace(',', '.')
                price = float(price)
                result['price'] = price
        except Exception as e:
            logging.warning(f"Exception when parsing price: {e}")

    @staticmethod
    def parse_categories(response, result):
        try:
            # category of product
            categories = response.css('ul.nav-list li a::text').getall()[1:2]

            for i, category in enumerate(categories):
                result[f"category_{i+1}"] = category
        except Exception as e:
            logging.warning(f"Exception when parsing categories: {e}")

    @staticmethod
    def parse_technical_details(response, result):
        try:
            # technical specification
            section = response.xpath('//section[@id="content-specs"]')

            rows = response.xpath('//section[@id="content-specs"] //table //tr').getall()
            """
            section = soup.find("section", id="content-specs")

            if section:
                table = section.find("table", class_="data-table")
    
                if table:
                    trs = table.find_all('tr')
                    for tr in trs:
                        th = tr.find('th')
                        td = tr.find('td')
                        label = th.get_text().strip()
                        value = td.get_text().strip()
                        product_item[label] = value
            """

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


