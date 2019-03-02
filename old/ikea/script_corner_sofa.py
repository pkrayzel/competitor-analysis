from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
import json


PRODUCT_DETAIL_PAGE_PREFIX = "https://www.ikea.com"

CATEGORIES_URL = {
        "corner_sofa": {
                "url": "https://www.ikea.com/nl/nl/hoekbanken.html?icid=a1:iba|a2:nl|a3:navigatie-producten|a4:banken-fauteuils-hoekbanken|a5:link|a6:hp|id:3007|cc:915",
        }
}


def clean_text(text):
        if text:
                return text.strip().replace('\t', '').replace('\n', '').replace('\r', '')
        return ''


def get_products_from_listing_page(category, config):
        
        if "file" not in config:
                listing_page_url = config["url"]
                response = requests.get(listing_page_url)
                content = response.content
        else:
                content_file = open(config["file"])
                content = content_file.read()
                content_file.close()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        products_ = soup.find_all("div", class_="bodyTextGray")

        products = []

        for item in products_:
                try:
                        start = time.time()

                        detail_link = item.find("a", class_="link-block")
                        data_section = item.find("section", {"data-inl-shoppable": "true"})

                        if not detail_link or not data_section:
                                continue

                        detail_url = detail_link["href"]

                        product_id = detail_url.split("/")[-2]

                        product_item = {
                                "product_id": product_id,
                                "detail_url": detail_url,
                                "category": category,
                                "competitor": "ikea"
                        }
                        products.append(product_item)
                        end = time.time()
                        print(f"Product basic info scraped in {end - start} seconds")
                except Exception as e:
                        print(f"Exception while getting data from listing page category: {category} - {e}")
        return products


def parse_detail_specification(product_item, soup):
        try:
                # product information
                product_item["product_type"] = soup.find("span", class_="productType").get_text()

                metrics = soup.find("div", id="metric").get_text()
                metrics = metrics.split("cm")

                for item in metrics:
                        try:
                                label, value = item.split(":")
                                value = clean_text(value)
                                product_item[label] = f"{value} cm"
                        except Exception as e:
                                pass
        except Exception as e:
                print(f"Exception parsing specification for product id {product_item['product_id']} - {e}")


def parse_price(product_item, soup):
        try:
                # product information

                price = soup.find("span", id="price1")

                if price:
                    price = price.get_text().replace('€ ', '').replace('.-', '').replace('\u20ac\u00a0', '')
                    product_item["price"] = price
        except Exception as e:
                print(f"Exception parsing specification for product id {product_item['product_id']} - {e}")


def parse_detail_description(product_item, soup):
        try:
                product_item["description"] = detail_page_soup.find("div", "salesArguments").get_text()
        except Exception as e:
                print(f"Exception parsing description for product id {product_item['product_id']} - {e}")


def save_final_output_file(products, category):
        output_file = open(f'output/ikea_{category}.json', 'w')
        json.dump(products, output_file)
        output_file.close()


start_time = time.time()

driver = webdriver.PhantomJS() # or add to your PATH
driver.set_window_size(1024, 768) # optional

for category, config in CATEGORIES_URL.items():
        print(f"====== {category} ======")
        
        products = get_products_from_listing_page(category, config)

        for product_item in products:
                product_start = time.time()
                
                # get detail url
                driver.get(product_item["detail_url"])

                detail_page_soup = BeautifulSoup(driver.page_source, 'html.parser')

                parse_detail_specification(product_item, detail_page_soup)

                parse_price(product_item, detail_page_soup)

                # description
                parse_detail_description(product_item, detail_page_soup)

                product_end = time.time()
                print(f"product scraped & saved in {product_end-product_start} seconds")
        save_final_output_file(products, category)
        print(f"====== {category} ======")

end_time = time.time()
difference = end_time - start_time
print(f'time of processing: {difference}')