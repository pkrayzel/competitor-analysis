from bs4 import BeautifulSoup
import requests
import time
import json


CATEGORIES_URL = {
        # "2_seat_sofas": {
        #     "urls": [
        #         "https://www.flinders.nl/wonen-banken-2-5-zitsbanken"
        #     ]
        # },
        "3_seat_sofas": {
            "urls": [
                "https://www.flinders.nl/wonen-banken-3-zitsbanken"
            ]
        },
        "corner_sofa": {
            "urls": [
                "https://www.flinders.nl/wonen-banken-hoekbanken"
            ]
        },
        "arm_chairs": {
            "urls": [
                "https://www.flinders.nl/wonen-stoelen-fauteuils"
            ]
        },
        "dining_chairs": {
            "urls": [
                "https://www.flinders.nl/wonen-stoelen-eetkamerstoelen",
                "https://www.flinders.nl/wonen-stoelen-eetkamerstoelen?p=2",
                "https://www.flinders.nl/wonen-stoelen-eetkamerstoelen?p=3",
                "https://www.flinders.nl/wonen-stoelen-eetkamerstoelen?p=4",
                "https://www.flinders.nl/wonen-stoelen-eetkamerstoelen?p=5",
            ]
        },
        # "beds": {
        #     "urls": [
        #         "https://www.flinders.nl/wonen-slaapkamer-tweepersoonsbedden",
        #         "https://www.flinders.nl/wonen-stoelen-fauteuils?p=2",
        #         "https://www.flinders.nl/wonen-stoelen-fauteuils?p=3",
        #     ]
        # },
        # "rugs": {
        #     "urls": [
        #         "https://www.flinders.nl/wonen-woonaccessoires-vloerkleden",
        #         "https://www.flinders.nl/wonen-woonaccessoires-vloerkleden?p=2",
        #         "https://www.flinders.nl/wonen-woonaccessoires-vloerkleden?p=3",
        #         "https://www.flinders.nl/wonen-woonaccessoires-vloerkleden?p=4",
        #         "https://www.flinders.nl/wonen-woonaccessoires-vloerkleden?p=5",
        #     ]
        # },
        # "pendant_lights": {
        #     "urls": [
        #         "https://www.flinders.nl/wonen-hanglampen",
        #         "https://www.flinders.nl/wonen-hanglampen?p=2",
        #         "https://www.flinders.nl/wonen-hanglampen?p=3",
        #         "https://www.flinders.nl/wonen-hanglampen?p=4",
        #         "https://www.flinders.nl/wonen-hanglampen?p=5",
        #     ]
        # },
        # "wall_lights": {
        #     "urls": [
        #         "https://www.flinders.nl/wonen-wandlampen",
        #         "https://www.flinders.nl/wonen-wandlampen?p=2",
        #         "https://www.flinders.nl/wonen-wandlampen?p=3",
        #         "https://www.flinders.nl/wonen-wandlampen?p=4",
        #         "https://www.flinders.nl/wonen-wandlampen?p=5",
        #     ]
        # },
        # "floor_lights": {
        #     "urls": [
        #         "https://www.flinders.nl/wonen-vloerlampen",
        #         "https://www.flinders.nl/wonen-vloerlampen?p=2",
        #         "https://www.flinders.nl/wonen-vloerlampen?p=3",
        #         "https://www.flinders.nl/wonen-vloerlampen?p=4",
        #         "https://www.flinders.nl/wonen-vloerlampen?p=5",
        #     ]
        # },
        # "table_lights": {
        #     "urls": [
        #         "https://www.flinders.nl/wonen-tafellampen",
        #         "https://www.flinders.nl/wonen-tafellampen?p=2",
        #         "https://www.flinders.nl/wonen-tafellampen?p=3",
        #         "https://www.flinders.nl/wonen-tafellampen?p=4",
        #         "https://www.flinders.nl/wonen-tafellampen?p=5",
        #     ]
        # },
}


def get_products_from_listing_page(category, config):
    result = []

    for url in config["urls"]:
        print(f"scraping url: {url}...")
        response = requests.get(url)
        content = response.content

        soup = BeautifulSoup(content, 'html.parser')

        products_ = soup.find_all("li", class_="item type-configurable")

        for item in products_:
            try:
                detail_link = item.find("a", {"data-gtmevent": "product-click"})
                detail_url = detail_link["href"]

                details_div = item.find("div", class_="details")
                title = details_div.find("span", class_="name").get_text()

                price = item.find("span", class_="price").get_text().strip().replace('€\xa0', '')

                product_item = {
                    "product_id": item["data-mpdb"],
                    "detail_url": detail_url,
                    "title": title.strip(),
                    "price": price,
                    "category": category,
                    "competitor": "flinders"
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
    except Exception as e:
        print(f"Exception parsing specification for product id {product_item['product_id']} - {e}")


def save_final_output_file(products, category):
    output_file = open(f'output/flinders_{category}.json', 'w')
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