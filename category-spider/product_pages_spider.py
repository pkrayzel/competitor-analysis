from datetime import datetime

# class ProductPagesSpider(scrapy.Spider):
#
#     name = 'product-pages'
#
#     custom_setting = {
#         "LOG_LEVEL": "INFO"
#     }
#
#     def start_requests(self):
#         for competitor in COMPETITORS:
#             for category, value in competitor.get_categories_urls().items():
#                 yield scrapy.Request(value['url'], meta={
#                     'country': competitor.country,
#                     'competitor': competitor.name,
#                     'category': category
#                 })
#
#     def parse(self, response):
#         competitor = find_competitor(response.meta['competitor'])
#         yield competitor.parse_category_details(response)
#
#     def closed(self, reason):
#         stats = self.crawler.stats.get_stats()
#         start_time = stats.get("start_time")
#         end_time = datetime.utcnow()
#         difference = end_time - start_time
#         self.logger.info(f"Total scraping time: {difference} seconds")


def handler(event, context):
    print(f"input event: {event}")

    return {
        "result": "success"
    }

if __name__ == "__main__":
    handler('', '')
