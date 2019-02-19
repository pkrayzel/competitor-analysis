from bs4 import BeautifulSoup
import requests
import time
import json


CATEGORIES_URL = {
        "2_seat_sofas": {
            "urls": [
                "https://www.vtwonen.nl/shop/meubels/banken/2-zits-banken",
                "https://www.vtwonen.nl/shop/meubels/banken/2-zits-banken?p=2",
                "https://www.vtwonen.nl/shop/meubels/banken/2-5-zits-banken",
                "https://www.vtwonen.nl/shop/meubels/banken/2-5-zits-banken?p=2"
            ]
        },
        "3_seat_sofas": {
            "urls": [
                "https://www.vtwonen.nl/shop/meubels/banken/3-zits-banken",
                "https://www.vtwonen.nl/shop/meubels/banken/3-zits-banken?p=2",
                "https://www.vtwonen.nl/shop/meubels/banken/3-zits-banken?p=3",
                "https://www.vtwonen.nl/shop/meubels/banken/3-5-zits-banken"
            ]
        },
        "corner_sofa": {
            "urls": [
                "https://www.vtwonen.nl/shop/meubels/banken/hoekbanken",
                "https://www.vtwonen.nl/shop/meubels/banken/hoekbanken?p=2"
            ]
        },
        "sofa_beds": {
            "urls": [
                "https://www.vtwonen.nl/shop/meubels/banken/bedbanken"
            ]
        },
        "arm_chairs": {
            "urls": [
                "https://www.vtwonen.nl/shop/meubels/stoelen/fauteuils",
                "https://www.vtwonen.nl/shop/meubels/stoelen/fauteuils?p=2",
                "https://www.vtwonen.nl/shop/meubels/stoelen/fauteuils?p=3"
            ]
        },
        # "accent_chairs": {
        #         "url": ""
        # },
        "dining_chairs": {
            "urls": [
                "https://www.vtwonen.nl/shop/meubels/stoelen/eetkamerstoelen",
                "https://www.vtwonen.nl/shop/meubels/stoelen/eetkamerstoelen?p=2",
                "https://www.vtwonen.nl/shop/meubels/stoelen/eetkamerstoelen?p=3",
                "https://www.vtwonen.nl/shop/meubels/stoelen/eetkamerstoelen?p=4",
                "https://www.vtwonen.nl/shop/meubels/stoelen/eetkamerstoelen?p=5",
                "https://www.vtwonen.nl/shop/meubels/stoelen/eetkamerstoelen?p=6",
            ]
        },
        "beds": {
            "urls": [
                "https://www.vtwonen.nl/shop/meubels/bedden/tweepersoonsbedden"
            ]
        },
        "boxspring_beds": {
            "urls": [
                "https://www.vtwonen.nl/shop/meubels/bedden/boxsprings"
            ]
        },
        "rugs": {
            "urls": [
                "https://www.vtwonen.nl/shop/wonen/vloerkleed",
                "https://www.vtwonen.nl/shop/wonen/vloerkleed?p=2",
                "https://www.vtwonen.nl/shop/wonen/vloerkleed?p=3",
                "https://www.vtwonen.nl/shop/wonen/vloerkleed?p=4",
                "https://www.vtwonen.nl/shop/wonen/vloerkleed?p=5",
                "https://www.vtwonen.nl/shop/wonen/vloerkleed?p=6",
                "https://www.vtwonen.nl/shop/wonen/vloerkleed?p=7",
                "https://www.vtwonen.nl/shop/wonen/vloerkleed?p=8",
                "https://www.vtwonen.nl/shop/wonen/vloerkleed?p=9",
                "https://www.vtwonen.nl/shop/wonen/vloerkleed?p=10",
            ]
        },
        "pendant_lights": {
            "urls": [
                "https://www.vtwonen.nl/shop/verlichting/hanglamp",
                "https://www.vtwonen.nl/shop/verlichting/hanglamp?p=2",
                "https://www.vtwonen.nl/shop/verlichting/hanglamp?p=3",
                "https://www.vtwonen.nl/shop/verlichting/hanglamp?p=4",
                "https://www.vtwonen.nl/shop/verlichting/hanglamp?p=5",
                "https://www.vtwonen.nl/shop/verlichting/hanglamp?p=6",
                "https://www.vtwonen.nl/shop/verlichting/hanglamp?p=6",
                "https://www.vtwonen.nl/shop/verlichting/hanglamp?p=7",
                "https://www.vtwonen.nl/shop/verlichting/hanglamp?p=8",
                "https://www.vtwonen.nl/shop/verlichting/hanglamp?p=9",
                "https://www.vtwonen.nl/shop/verlichting/hanglamp?p=10",
                "https://www.vtwonen.nl/shop/verlichting/hanglamp?p=11",
                "https://www.vtwonen.nl/shop/verlichting/hanglamp?p=12",
                "https://www.vtwonen.nl/shop/verlichting/hanglamp?p=13",
            ]
        },
        "wall_lights": {
            "urls": [
                "https://www.vtwonen.nl/shop/verlichting/wandlampen",
                "https://www.vtwonen.nl/shop/verlichting/wandlampen?p=2",
                "https://www.vtwonen.nl/shop/verlichting/wandlampen?p=3",
                "https://www.vtwonen.nl/shop/verlichting/wandlampen?p=4"
            ]
        },
        "floor_lights": {
            "urls": [
                "https://www.vtwonen.nl/shop/verlichting/vloerlampen",
                "https://www.vtwonen.nl/shop/verlichting/vloerlampen?p=2",
                "https://www.vtwonen.nl/shop/verlichting/vloerlampen?p=3",
                "https://www.vtwonen.nl/shop/verlichting/vloerlampen?p=4",
            ]
        },
        "table_lights": {
            "urls": [
                "https://www.vtwonen.nl/shop/verlichting/tafellampen",
                "https://www.vtwonen.nl/shop/verlichting/tafellampen?p=2",
                "https://www.vtwonen.nl/shop/verlichting/tafellampen?p=3",
                "https://www.vtwonen.nl/shop/verlichting/tafellampen?p=4",
                "https://www.vtwonen.nl/shop/verlichting/tafellampen?p=5",
                "https://www.vtwonen.nl/shop/verlichting/tafellampen?p=6",
                "https://www.vtwonen.nl/shop/verlichting/tafellampen?p=7"
            ]
        },
}


def get_products_from_listing_page(category, config):
    result = []

    for url in config["urls"]:
        print(f"scraping url: {url}...")
        response = requests.get(url)
        content = response.content

        soup = BeautifulSoup(content, 'html.parser')

        products_ = soup.find_all("div", class_="product-item-info product-item-info-grid")

        for item in products_:
            try:
                detail_link = item.find("a", class_="product-item-link")
                title = detail_link.get_text()
                detail_url = detail_link["href"]

                price_box = item.find("div", class_="price-box price-final_price")

                product_id = price_box["data-product-id"]

                price = item.find("span", class_="price").get_text().strip()

                product_item = {
                    "product_id": product_id,
                    "detail_url": detail_url,
                    "title": title.strip(),
                    "price": price,
                    "category": category,
                    "competitor": "vtonen"
                }
                result.append(product_item)
            except Exception as e:
                print(f"Exception while getting data from listing page category: {category} - {e}")

    return result


def store_detail_page_to_file(category, product_id, file_content):
    tmp_file = open(f'tmp_output/{category}_{product_id}.txt', 'w')
    tmp_file.write(file_content.decode("UTF-8"))
    tmp_file.close()


def parse_detail_specification(product_item, soup):
    try:
        data_items = soup.find_all("dd", class_="col data")

        for item in data_items:
            label = item["data-th"]
            value = item.get_text()
            product_item[label] = value
    except Exception as e:
        print(f"Exception parsing specification for product id {product_item['product_id']} - {e}")


def save_final_output_file(products, category):
    output_file = open(f'output/vtonen_{category}.json', 'w')
    json.dump(products, output_file)
    output_file.close()


start_time = time.time()


for category, config in CATEGORIES_URL.items():
    print(f"====== {category} ======")

    products = get_products_from_listing_page(category, config)

    print(f"Found: {len(products)} products")
    for product_item in products:
        product_start = time.time()
        # get detail url
        response = requests.get(product_item["detail_url"])

        detail_page_soup = BeautifulSoup(response.content, 'html.parser')

        parse_detail_specification(product_item, detail_page_soup)

        product_end = time.time()
        print(f"product scraped & saved in {product_end-product_start} seconds")

    save_final_output_file(products, category)
    print(f"====== {category} ======")

end_time = time.time()
difference = end_time - start_time
print(f'time of processing: {difference}')