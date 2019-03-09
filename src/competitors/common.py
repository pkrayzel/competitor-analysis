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

    def convert_to_csv_item(self, product_page_item):
        result = dict(country=product_page_item["country"],
                      competitor=product_page_item["competitor"],
                      category=product_page_item["category"],
                      price=product_page_item["product_info"]["price"],
                      title=product_page_item["product_info"]["title"])
        return result

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

