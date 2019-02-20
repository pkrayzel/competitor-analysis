from bs4 import BeautifulSoup
import requests
import time
import json

PREFIX_URL = "https://www.sofa.com"

CATEGORIES_URL = {
        "2_seat_sofas": {
            "urls": [
                "https://www.sofa.com/nl/banken/2-zits",
                "https://www.sofa.com/nl/banken/2-en-half-zits"
            ]
        },
        "3_seat_sofas": {
            "urls": [
                "https://www.sofa.com/nl/banken/3-zits"
            ]
        },
        # "corner_sofa": {
        #     "urls": [
        #         "https://www.sofa.com/nl/banken/hoekbanken"
        #     ]
        # },
        # "sofa_beds": {
        #     "urls": [
        #         "https://www.sofa.com/nl/banken/slaapbanken"
        #     ]
        # },
        # "arm_chairs": {
        #     "urls": [
        #         "https://www.sofa.com/nl/fauteuils"
        #     ]
        # },
        # "beds": {
        #     "urls": [
        #         "https://www.sofa.com/nl/bedden/tweepersoons",
        #         "https://www.sofa.com/nl/bedden/king",
        #         "https://www.sofa.com/nl/bedden/super-king",
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

        products_ = soup.find_all("div", class_="product-item")

        for item in products_:
            try:
                title = item.find("input", {"name": "productName"})["value"]
                product_id = item.find("input", {"name": "productCode"})["value"]
                sofa_category = item.find("input", {"name": "categoryName"})["value"]

                detail_link = item.find("a", class_="thumb")
                detail_url = detail_link["href"]

                product_item = {
                    "product_id": product_id,
                    "detail_url": PREFIX_URL + detail_url,
                    "title": title,
                    "category": category,
                    "sofa_category": sofa_category,
                    "competitor": "sofa"
                }
                result.append(product_item)
                print(product_item)
            except Exception as e:
                print(f"Exception while getting data from listing page category: {category} - {e}")

    return result


def store_detail_page_to_file(category, product_id, file_content):
    tmp_file = open(f'tmp_output/{category}_{product_id}.txt', 'w')
    tmp_file.write(file_content.decode("UTF-8"))
    tmp_file.close()


def parse_prices(product_item, soup):
    try:
        div = soup.find("div", id="productPrice")
        if div:
            was_price = div.find("span", class_="price-txt__price price-txt__wasprice")

            if was_price:
                was_price = was_price.get_text().strip().replace('€ ', '')
                product_item["original_price"] = was_price

            now_price = div.find("span", class_="price-txt__price price-txt__nowprice")

            if now_price:
                now_price = now_price.get_text().strip().replace('€ ', '')

                if "Was" in now_price:
                    now_price = now_price.split("Was")[0]
                    now_price = now_price.replace('\r\n', '').strip()

                product_item["price"] = now_price

    except Exception as e:
        print(f"Exception parsing specification for product id {product_item['product_id']} - {e}")


def parse_detail_specification(product_item, soup):
    try:
        div = soup.find("div", class_="sizeDetailsContent")

        if div:
            tables = div.find_all("table")

            for t in tables:
                trs = t.find_all('tr')

                for tr in trs:
                    tds = tr.find_all('td')
                    label = tds[0].get_text().strip()
                    value = tds[1].get_text().strip()
                    product_item[label] = value
    except Exception as e:
        print(f"Exception parsing specification for product id {product_item['product_id']} - {e}")


def save_final_output_file(products, category):
    output_file = open(f'output/sofa_{category}.json', 'w')
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

        parse_prices(product_item, detail_page_soup)

        product_end = time.time()
        print(f"product scraped & saved in {product_end-product_start} seconds")

    save_final_output_file(products, category)
    print(f"====== {category} ======")

end_time = time.time()
difference = end_time - start_time
print(f'time of processing: {difference}')