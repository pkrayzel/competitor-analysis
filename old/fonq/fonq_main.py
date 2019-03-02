from bs4 import BeautifulSoup
import requests
import time
import json


PREFIX_URL = "https://www.fonq.nl"

CATEGORIES_URL = {
        "2_seat_sofas": { "url": "https://www.fonq.nl/producten/categorie-2_zitsbank/" },
        "3_seat_sofas": { "url": "https://www.fonq.nl/producten/categorie-3_zitsbank/" },
        "corner_sofa": { "url": "https://www.fonq.nl/producten/categorie-hoekbank/" },
        "sofa_beds": { "url": "https://www.fonq.nl/producten/categorie-slaapbanken/" },
        "arm_chairs": { "url": "https://www.fonq.nl/producten/categorie-fauteuil/" },
        "dining_chairs": { "url": "https://www.fonq.nl/producten/categorie-eetkamerstoel/" },
        "beds": { "url": "https://www.fonq.nl/producten/categorie-tweepersoonsbedden/?ms_fk_model=Tweepersoons&templateid=1452" },
        "boxspring_beds": { "url": "https://www.fonq.nl/producten/categorie-bedden/?ms_fk_model=Tweepersoons&templateid=1452" },
        "rugs": { "url": "https://www.fonq.nl/producten/categorie-vloerkleden/vorm-rechthoekig/" },
        "pendant_lights": { "url": "https://www.fonq.nl/producten/categorie-hanglampen/" },
        "wall_lights": { "url": "https://www.fonq.nl/producten/categorie-wandlampen/" },
        "floor_lights": { "url": "https://www.fonq.nl/producten/categorie-vloerlampen/" },
        "table_lights": { "url": "https://www.fonq.nl/producten/categorie-tafellampen/" },
}


def get_products_from_listing_page(category, config):
    result = []
    for url in config["urls"]:
        print(f"scraping url: {url}...")
        response = requests.get(url)
        content = response.content

        soup = BeautifulSoup(content, 'html.parser')

        products_ = soup.find_all("div", class_="product-new")

        for item in products_:
            try:
                detail_link = item.find("a", class_="link-muted")
                detail_url = detail_link["href"]
                title = detail_link.get_text()

                # product_id = detail_url.split('/')[-2]

                product_item = {
                    "detail_url": PREFIX_URL + detail_url,
                    "title": title.strip(),
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
        div = soup.find("div", id="product-specs")

        if div:
            tables = div.find_all("table")

            print(f"{product_item['product_id']} - tables: {len(tables)}")

            for t in tables:
                trs = t.find_all('tr')
                for tr in trs:
                    tds = tr.find_all('td')
                    label = tds[0].get_text().strip()
                    value = tds[1].get_text().strip()
                    product_item[label] = value

    except Exception as e:
        print(f"Exception parsing technical specification detail for product id: {product_item['product_id']} - {e}")

    return product_item

def save_output_file(product_item, category):
    output_file = open(f'output/{category}/{product_item["product_id"]}.json', 'w')
    json.dump(product_item, output_file)
    output_file.close()


def parse_product(product_item, category):
    product_start = time.time()
    # get detail url
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"
    }
    response = requests.get(product_item["detail_url"], headers=headers)

    if response.status_code != 200:
        print(f"ERROR: {response.status_code}")
        time.sleep(1)
        response = requests.get(product_item["detail_url"])
        print(f"Status code retry: {response.status_code}")

    detail_page_soup = BeautifulSoup(response.content, 'html.parser')

    item = parse_detail_specification(product_item, detail_page_soup)

    product_end = time.time()
    save_output_file(item, category)
    print(f"product scraped & saved in {product_end-product_start} seconds")


def main():
    start_time = time.time()
    for category, config in CATEGORIES_URL.items():
        print(f"====== {category} ======")

        products = get_products_from_listing_page(category, config)

        with open('output.json', 'w') as output:
            json.dump(products, output, indent=4)
        # for p in products:
        #     parse_product(p, category)
    end_time = time.time()
    print(f"difference: {end_time-start_time} seconds")

if __name__ == "__main__":
  main()
