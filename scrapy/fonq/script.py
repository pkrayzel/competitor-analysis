import scrapy


class FonqSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'https://www.fonq.nl/producten/categorie-2_zitsbank/',
        'https://www.fonq.nl/producten/categorie-2_zitsbank/?p=2',
        'https://www.fonq.nl/producten/categorie-2_zitsbank/?p=3',
    ]

    def parse(self, response):
        products = response.css('div.product-new')

        next_pages = []
        for p in products:
            detail_link = p.css('a.link-muted::attr(href)').get()
            yield {
                'detail_link': detail_link,
                'title': p.css('a.link-muted::text').get()
            }
            next_pages.append(detail_link)

        for page in next_pages:
            next_page = response.urljoin(page)
            yield scrapy.Request(next_page, callback=self.parse_product_detail)

    def parse_product_detail(self, response):
        print(response.body)