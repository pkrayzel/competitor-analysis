from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
import json


PRODUCT_DETAIL_PAGE_PREFIX = "https://www.ikea.com"

CATEGORIES_URL = {
        "2_seat_sofas": {
                "url": "https://www.ikea.com/nl/nl/catalog/categories/departments/living_room/10668/?icid=a1:iba|a2:nl|a3:navigatie-producten|a4:banken-fauteuils-2-zitsbanken|a5:link|a6:hp|id:3012|cc:915",
        },
        # "3_seat_sofas": {
        #         "url": "",
        # },
        # !!! bit different design
        # "corner_sofa": {
        #         "url": "https://www.ikea.com/nl/nl/hoekbanken.html?icid=a1:iba|a2:nl|a3:navigatie-producten|a4:banken-fauteuils-hoekbanken|a5:link|a6:hp|id:3007|cc:915",
        # },
        "sofa_beds": {
                "url": "https://www.ikea.com/nl/nl/catalog/categories/departments/living_room/10663/?icid=a1:iba|a2:nl|a3:navigatie-producten|a4:banken-fauteuils-slaapbanken|a5:link|a6:hp|id:3008|cc:915",
        },
        "arm_chairs": {
                "url": "https://www.ikea.com/nl/nl/catalog/categories/departments/living_room/16239/?icid=a1:iba|a2:nl|a3:navigatie-producten|a4:banken-fauteuils-fauteuils|a5:link|a6:hp|id:3009|cc:915",
        },
        # "accent_chairs": {
        #         "url": "",
        # },
        "dining_chairs": {
                "url": "https://www.ikea.com/nl/nl/catalog/categories/departments/dining/25219/?icid=a1:iba|a2:nl|a3:navigatie-producten|a4:tafels-stoelen-eetkamerstoelen|a5:link|a6:hp|id:3112|cc:915",
        },
        "Double_beds": {
                "url": "https://www.ikea.com/nl/nl/catalog/categories/departments/bedroom/16284/?icid=a1:iba|a2:nl|a3:navigatie-producten|a4:boxsprings-bedden-matrassen-tweepersoonsbedden|a5:link|a6:hp|id:4036|cc:915",
        },
        # "king_size_beds": {
        #         "url": "",
        # },
        # "super_king_size_beds": {
        #         "url": "",
        # },
        "boxspring_beds": {
                "url": "https://www.ikea.com/nl/nl/catalog/categories/departments/bedroom/28433/?icid=a1:iba|a2:nl|a3:navigatie-producten|a4:boxsprings-bedden-matrassen-boxsprings|a5:link|a6:hp|id:3074|cc:915",
        },
        "sofa_beds": {
                "url": "https://www.ikea.com/nl/nl/catalog/categories/departments/living_room/10663/?icid=a1:iba|a2:nl|a3:navigatie-producten|a4:banken-fauteuils-slaapbanken|a5:link|a6:hp|id:3008|cc:915",
        },
        "rugs": {
                "url": "https://www.ikea.com/nl/nl/catalog/categories/departments/Textiles/10653/?icid=a1:iba|a2:nl|a3:navigatie-producten|a4:vloerenenvloerkleden-vloerkleden|a5:link|a6:hp|id:3162|cc:915",
        },
        "pendant_lights": {
                "url": "https://www.ikea.com/nl/nl/catalog/categories/departments/lighting/18750/?icid=a1:iba|a2:nl|a3:navigatie-producten|a4:verlichting-hanglampen|a5:link|a6:hp|id:3098|cc:915",
        },
        "wall_lights": {
                "url": "https://www.ikea.com/nl/nl/catalog/categories/departments/lighting/20503/?icid=a1:iba|a2:nl|a3:navigatie-producten|a4:verlichting-wandlampen|a5:link|a6:hp|id:3100|cc:915",
        },
        "floor_lights": {
                "url": "https://www.ikea.com/nl/nl/catalog/categories/departments/lighting/10731/?icid=a1:iba|a2:nl|a3:navigatie-producten|a4:verlichting-staande-lampen|a5:link|a6:hp|id:3101|cc:915",
        },
        "table_lights": {
                "url": "https://www.ikea.com/nl/nl/catalog/categories/departments/lighting/10732/?icid=a1:iba|a2:nl|a3:navigatie-producten|a4:verlichting-tafellampen|a5:link|a6:hp|id:3103|cc:915",
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
        
        products_ = soup.find_all("div", class_="threeColumn")

        products = []

        for item in products_:
                try:
                        start = time.time()

                        if "product" not in item["class"]:
                                continue

                        detail_link = item.find("a", class_="productLink")
                        title = item.find("span", class_="productTitle").get_text()
                        detail_url = detail_link["href"]
                        product_id = detail_url.split("/")[-2]
                        price = clean_text(item.find("span", class_="price regularPrice").get_text())
                        price = price.replace('/st.Prijs per set', '').replace('€\xa0', '').replace('.-', '')

                        product_item = {
                                "product_id": product_id,
                                "detail_url": PRODUCT_DETAIL_PAGE_PREFIX + detail_url,
                                "title": title.strip(),
                                "price": price,
                                "category": category,
                                "competitor": "ikea"
                        }
                        products.append(product_item)
                        end = time.time()
                        print(f"Product basic info scraped in {end - start} seconds")

                except Exception as e:
                        print(f"Exception while getting data from listing page category: {category} - {e}")
        return products


def store_detail_page_to_file(category, product_id, file_content):
        tmp_file = open(f'tmp_output/{category}_{product_id}.txt', 'w')
        tmp_file.write(driver.page_source)
        tmp_file.close()


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


def parse_detail_description(product_item, soup):
        try:
                product_item["description"] = detail_page_soup.find("div", "salesArguments").get_text()
        except Exception as e:
                print(f"Exception parsing description for product id {product_item['product_id']} - {e}")


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

        for product_item in products:
                product_start = time.time()
                
                # get detail url
                driver.get(product_item["detail_url"])
                # store it to a temp file
                store_detail_page_to_file(
                        category=category, 
                        product_id=product_item["product_id"],
                        file_content=driver.page_source
                )

                detail_page_soup = BeautifulSoup(driver.page_source, 'html.parser')

                parse_detail_specification(product_item, detail_page_soup)

                # description
                parse_detail_description(product_item, detail_page_soup)

                product_end = time.time()
                print(f"product scraped & saved in {product_end-product_start} seconds")
        save_final_output_file(products, category)
        print(f"====== {category} ======")

end_time = time.time()
difference = end_time - start_time
print(f'time of processing: {difference}')