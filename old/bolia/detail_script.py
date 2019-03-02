from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json
import os
import multiprocessing as mp

BOLIA_URL_PREFIX = "https://www.bolia.com"


driver = webdriver.PhantomJS() # or add to your PATH


def get_products_from_file(filename):
    with open(filename) as f:
        data = json.load(f)

    return data


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


def parse_one_product(product_item, category):
    product_start = time.time()
        # get detail url
    driver.get(product_item["detail_url"])
    try:
        driver.find_element_by_class_name("c-product-bar__nav-item").click()
    except Exception as e:
        print(f"Can't click specification button: {e}")

    detail_page_soup = BeautifulSoup(driver.page_source, 'html.parser')
    parse_price(product_item, detail_page_soup)
    parse_detail_specification(product_item, detail_page_soup)

    save_output_file(product_item, category)

    product_end = time.time()
    print(f"product scraped & saved in {product_end-product_start} seconds")



def save_output_file(product_item, category):
    output_file = open(f'output/{category}/{product_item["product_id"]}.json', 'w')
    json.dump(product_item, output_file)
    output_file.close()


def main():

    for subdir, dirs, files in os.walk("input/"):
        for filename in files:
            start_time = time.time()

            products = get_products_from_file("input/" + filename)
            category = filename.replace('bolia_', '').replace('.json', '')
            for p in products:
                parse_one_product(p, category)

            end_time = time.time()
            difference = end_time - start_time
            print(f'time of processing: {difference}')

if __name__ == "__main__":
    main()