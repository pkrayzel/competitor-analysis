from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
import json


PRODUCT_DETAIL_PAGE_PREFIX = "https://loods5.nl"

CATEGORIES_URL = {
        # "2_seat_sofas": {
        #         "url": "https://loods5.nl/shop/meubels/stoelen-banken/banken?prijs-vanaf=149&prijs-tot=8326&zits=391",
        # },
        # "3_seat_sofas": {
        #         "url": "https://loods5.nl/shop/meubels/stoelen-banken/banken?prijs-vanaf=149&prijs-tot=8326&zits=394,395",
        #         "file": "input/3_seat_sofas.html"
        # },
        # "corner_sofa": {
        #         "url": "https://loods5.nl/shop/meubels/stoelen-banken/banken?prijs-vanaf=149&prijs-tot=8326&zits=76,77,78",
        # },
        # "sofa_beds": {
        #         "url": "https://loods5.nl/shop/meubels/stoelen-banken/banken?prijs-vanaf=149&prijs-tot=8326&zits=80",
        # },
        # "arm_chairs": {
        #         "url": "https://loods5.nl/shop/meubels/stoelen-banken/fauteuils",
        #         "file": "input/arm_chairs.html"
        # },
        # "dining_chairs": {
        #         "url": "https://loods5.nl/shop/meubels/stoelen-banken/stoelen",
        #         "file": "input/dining_chairs.html"
        # },
        "rugs": {
                "url": "https://loods5.nl/zoeken?vind=rugs",
                "file": "rugs.htm"
        },
        "pendant_lights": {
                "url": "https://loods5.nl/shop/verlichting/verlichting/hanglampen",
                "file": "pendant_lights.htm"
        },
        "wall_lights": {
                "url": "https://loods5.nl/shop/verlichting/verlichting/wandlampen",
                "file": "wall_lights.htm"
        },
        "floor_lights": {
                "url": "https://loods5.nl/shop/verlichting/verlichting/vloerlampen",
                "file": "floor_lights.htm"
        },
        "table_lights": {
                "url": "https://loods5.nl/shop/verlichting/verlichting/tafel-bureaulampen",
                "file": "table_lights.htm"
        },
}

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
        
        products_ = soup.find_all("div", class_="product-item")

        products = []
        for item in products_:
                try:
                        start = time.time()
                        css_class = item["class"]
                        if not "product-item" in css_class or "col-25" not in css_class:
                                continue

                        detail_link = item.find("a", class_="wide product--details-link")
                        title = detail_link.get_text()
                        detail_url = detail_link["href"]
                        product_id = detail_url.split("/")[-1]
                        currency = item.find("span", class_="currency").get_text()
                        price = item.find("span", class_="price").get_text().strip().replace('\n', '').replace(' ', '').replace(currency, '')
                        
                        product_item = {
                                "product_id": product_id,
                                "detail_url": PRODUCT_DETAIL_PAGE_PREFIX + detail_url,
                                "title": title.strip(),
                                "price": price,
                                "category": category,
                                "competitor": "loods_5"
                        }
                        products.append(product_item)
                        end = time.time()
                        print(f"Product basic info scraped in {end - start} seconds")
                except Exception as e:
                        print(f"Exception while getting data from listing page category: {category} - {e}")
        return products


def parse_detail_specification(product_item, soup):
        try:
                # specification
                specification_labels = soup.find_all("span", class_="product-page-specs--spec--label")
                specification_values = soup.find_all("span", class_="product-page-specs--spec--value")
                
                for i in range(len(specification_labels)):
                        label = specification_labels[i].get_text().strip()
                        value = specification_values[i].get_text().strip()
                        product_item[label] = value
        except Exception as e:
                print(f"Exception parsing specification for product id {product_item['product_id']} - {e}")


def parse_detail_description(product_item, soup):
        try:
                product_item["description"] = detail_page_soup.find("div", "product-description").find("p").get_text()
        except Exception as e:
                print(f"Exception parsing description for product id {product_item['product_id']} - {e}")


def parse_detail_main_features(product_item, soup):
        try:
                main_features = detail_page_soup.find("div", "product-main-features").find_all("li")
                                
                for li in main_features:
                        li_text = li.get_text()
                        if ":" in li_text:
                                key, value = li_text.split(":")
                                product_item[key] = value
        except Exception as e:
                print(f"Exception parsing main features for product id {product_item['product_id']} - {e}")


def save_final_output_file(products, category):
        output_file = open(f'output/loods5_{category}.json', 'w')
        json.dump(products, output_file)
        output_file.close()


start_time = time.time()

driver = webdriver.PhantomJS() # or add to your PATH
driver.set_window_size(1024, 768) # optional

for category, config in CATEGORIES_URL.items():
        print(f"====== {category} ======")
        
        products = get_products_from_listing_page(category, config)
        
        print(len(products))
        for product_item in products:
                product_start = time.time()
                
                # get detail url
                driver.get(product_item["detail_url"])

                detail_page_soup = BeautifulSoup(driver.page_source, 'html.parser')

                parse_detail_specification(product_item, detail_page_soup)

                # description
                parse_detail_description(product_item, detail_page_soup)
                
                # main features 
                parse_detail_main_features(product_item, detail_page_soup)

                product_end = time.time()
                print(f"product scraped & saved in {product_end-product_start} seconds")
        
        save_final_output_file(products, category)
        print(f"====== {category} ======")

end_time = time.time()
difference = end_time - start_time
print(f'time of processing: {difference}')