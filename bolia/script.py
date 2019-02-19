from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json


BOLIA_URL_PREFIX = "https://www.bolia.com"


CATEGORIES_URL = {
        # "2_seat_sofas": {
        #     "urls": [
        #         "https://www.bolia.com/nl-nl/banken/alle-banken/?Model=2-zitsbank&Model=2%C2%BD-zitsbank&size=1000"
        #     ]
        # },
        # "3_seat_sofas": {
        #     "urls": [
        #         "https://www.bolia.com/nl-nl/banken/alle-banken/?Category=Banken&Model=3-zitsbank&size=1000"
        #     ]
        # },
        # "corner_sofa": {
        #     "urls": [
        #         "https://www.bolia.com/nl-nl/banken/hoekbanken/?size=1000"
        #     ]
        # },
        # "sofa_beds": {
        #     "urls": [
        #         "https://www.bolia.com/nl-nl/banken/slaapbanken/?Category=Slaapbanken&Chaise%20OE=Zonder%20chaise%20longue%20en%20open%20end&size=1000"
        #     ]
        # },
        # "arm_chairs": {
        #     "urls": [
        #         "https://www.bolia.com/nl-nl/meubels/woonkamer/fauteuils/?Category=Fauteuils&size=1000"
        #     ]
        # },
        # "dining_chairs": {
        #     "urls": [
        #         "https://www.bolia.com/nl-nl/meubels/eetkamer/eetkamerstoelen/?Category=Eetkamerstoelen&size=1000",
        #     ]
        # },
        # "pendant_lights": {
        #     "urls": [
        #         "https://www.bolia.com/nl-nl/accessoires/lampen/hanglampen/?Family=Arita&Family=Ball&Family=Balloon&Family=Bell-A&Family=Bulb&Family=Cover&Family=Cyla&Family=Flachmann&Family=Glasblase&Family=Grape&Family=In%20Circles&Family=LED%20bulb&Family=Leaves&Family=Maiko&Family=Orb&Family=Pica&Family=Piper&Family=Pop&Family=Rotate&Family=Slice&Family=Squeeze&Family=Vetro",
        #     ]
        # },
        # "wall_lights": {
        #     "urls": [
        #         "https://www.bolia.com/nl-nl/accessoires/lampen/wandlampen/?Material=Glas&Material=Marmer&Material=Staal"
        #     ]
        # },
        # "floor_lights": {
        #     "urls": [
        #         "https://www.bolia.com/nl-nl/accessoires/lampen/vloerlampen/?Material=Acryl&Material=Glas&Material=Marmer&Material=Staal",
        #     ]
        # },
        # "table_lights": {
        #     "urls": [
        #         "https://www.bolia.com/nl-nl/accessoires/lampen/tafellampen/?Material=Beton&Material=Glas&Material=Marmer&Material=Staal"
        #     ]
        # },
}

driver = webdriver.PhantomJS() # or add to your PATH


def get_products_from_listing_page(category, config):
    result = []

    for url in config["urls"]:
        print(f"scraping url: {url}...")
        driver.get(url)
        content = driver.page_source

        soup = BeautifulSoup(content, 'html.parser')

        detail_links = soup.find_all("a", class_="absolute pin cursor-pointer")

        for item in detail_links:
            link = f'{BOLIA_URL_PREFIX}{item["href"]}'
            product_id = link.split("/")[-1]

            product_item = {
                "product_id": product_id,
                "detail_url": link,
                "category": category,
                "competitor": "bolia"
            }
            result.append(product_item)

    return result


def store_detail_page_to_file(category, product_id, file_content):
    tmp_file = open(f'tmp_output/{category}_{product_id}.txt', 'w')
    tmp_file.write(file_content)
    tmp_file.close()


def parse_detail_specification(product_item, soup):
    try:
        data_labels = soup.find_all("dt", {"ng-bind": "spec.title"})
        data_values = soup.find_all("dd", {"ng-bind": "spec.desc"})

        for i in range(len(data_labels)):
            label = data_labels[i].get_text()
            value = data_values[i].get_text()
            product_item[label] = value

    except Exception as e:
        print(f"Exception parsing specification for product id {product_item['product_id']} - {e}")


def parse_price(product_item, soup):
    try:
        prices = soup.find_all("span", {"ng-bind": "$ctrl.product.salesPrice.amount"})

        sales_price = 0

        if prices:
            sales_price = prices[0].get_text().replace('\u20ac ', '')

        product_item["sales_price"] = sales_price

        original_prices = soup.find_all("p", {"ng-if": "$ctrl.product.listPrice.amount !== $ctrl.product.salesPrice.amount"})

        if original_prices:
            price = original_prices[0].get_text().replace('\u20ac ', '')
            price = price.replace('Normaal', '').strip()
            product_item["original_price"] = price.split('\n')[0]
        else:
            product_item["original_price"] = product_item["sales_price"]

    except Exception as e:
        print(f"Exception parsing specification for product id {product_item['product_id']} - {e}")



def save_final_output_file(products, category):
    output_file = open(f'output/bolia_{category}.json', 'w')
    json.dump(products, output_file)
    output_file.close()


start_time = time.time()


for category, config in CATEGORIES_URL.items():
    print(f"====== {category} ======")

    products = []

    for i in range(5):
        products = get_products_from_listing_page(category, config)

        if len(products) > 0:
            break

        time.sleep(2)
        print(f"Found: {len(products)} products - retrying...")

    print(f"Found: {len(products)} products")
    save_final_output_file(products, category)

    # for product_item in products:
    #     product_start = time.time()
    #     # get detail url
    #     driver.get(product_item["detail_url"])
    #     try:
    #         driver.find_element_by_class_name("c-product-bar__nav-item").click()
    #         parse_detail_specification(product_item, detail_page_soup)
    #     except Exception as e:
    #         print(f"Can't click specification button: {e}")
    #
    #     detail_page_soup = BeautifulSoup(driver.page_source, 'html.parser')
    #     parse_price(product_item, detail_page_soup)
    #
    #     product_end = time.time()
    #     print(f"product scraped & saved in {product_end-product_start} seconds")
    #
    # save_final_output_file(products, category)
    # print(f"====== {category} ======")

end_time = time.time()
difference = end_time - start_time
print(f'time of processing: {difference}')