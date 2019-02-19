from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time
import json

PREFIX_URL = "https://www.fonq.nl"

CATEGORIES_URL = {
        "2_seat_sofas": {
            "urls": [
                "https://www.fonq.nl/producten/categorie-2_zitsbank/",
                "https://www.fonq.nl/producten/categorie-2_zitsbank/?p=2",
                "https://www.fonq.nl/producten/categorie-2_zitsbank/?p=3"
            ]
        },
        # "3_seat_sofas": {
        #     "urls": [
        #         "https://www.fonq.nl/producten/categorie-3_zitsbank/",
        #         "https://www.fonq.nl/producten/categorie-3_zitsbank/?p=2",
        #         "https://www.fonq.nl/producten/categorie-3_zitsbank/?p=3",
        #         "https://www.fonq.nl/producten/categorie-3_zitsbank/?p=4"
        #     ]
        # },
        # "corner_sofa": {
        #     "urls": [
        #         "https://www.fonq.nl/producten/categorie-hoekbank/",
        #         "https://www.fonq.nl/producten/categorie-hoekbank/?p=2"
        #     ]
        # },
        # "sofa_beds": {
        #     "urls": [
        #         "https://www.fonq.nl/producten/categorie-slaapbanken/",
        #         "https://www.fonq.nl/producten/categorie-slaapbank/?p=2",
        #         "https://www.fonq.nl/producten/categorie-slaapbank/?p=3",
        #         "https://www.fonq.nl/producten/categorie-slaapbank/?p=4",
        #         "https://www.fonq.nl/producten/categorie-slaapbank/?p=5",
        #     ]
        # },
        # "arm_chairs": {
        #     "urls": [
        #         "https://www.fonq.nl/producten/categorie-fauteuil/",
        #         "https://www.fonq.nl/producten/categorie-fauteuil/?p=2",
        #         "https://www.fonq.nl/producten/categorie-fauteuil/?p=3",
        #         "https://www.fonq.nl/producten/categorie-fauteuil/?p=4",
        #         "https://www.fonq.nl/producten/categorie-fauteuil/?p=5",
        #         "https://www.fonq.nl/producten/categorie-fauteuil/?p=6",
        #         "https://www.fonq.nl/producten/categorie-fauteuil/?p=7",
        #         "https://www.fonq.nl/producten/categorie-fauteuil/?p=8",
        #         "https://www.fonq.nl/producten/categorie-fauteuil/?p=9",
        #         "https://www.fonq.nl/producten/categorie-fauteuil/?p=10",
        #         "https://www.fonq.nl/producten/categorie-fauteuil/?p=11",
        #         "https://www.fonq.nl/producten/categorie-fauteuil/?p=12",
        #         "https://www.fonq.nl/producten/categorie-fauteuil/?p=13",
        #         "https://www.fonq.nl/producten/categorie-fauteuil/?p=14",
        #         "https://www.fonq.nl/producten/categorie-fauteuil/?p=15",
        #     ]
        # },
        # "dining_chairs": {
        #     "urls": [
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=2",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=3",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=4",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=5",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=6",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=7",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=8",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=9",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=10",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=11",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=12",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=13",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=14",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=15",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=16",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=17",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=18",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=19",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=20",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=21",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=22",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=23",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=24",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=25",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=26",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=27",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=28",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=29",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=30",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=31",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=32",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=33",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=34",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=35",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=36",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=37",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=38",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=39",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=40",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=41",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=42",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=43",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=44",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=45",
        #         "https://www.fonq.nl/producten/categorie-eetkamerstoel/?p=46",
        #     ]
        # },
        # "beds": {
        #     "urls": [
        #         "https://www.fonq.nl/producten/categorie-tweepersoonsbedden/?ms_fk_model=Tweepersoons&templateid=1452"
        #     ]
        # },
        # "boxspring_beds": {
        #     "urls": [
        #         "https://www.fonq.nl/producten/categorie-bedden/?ms_fk_model=Tweepersoons&templateid=1452",
        #         "https://www.fonq.nl/producten/categorie-bedden/?ms_fk_model=Tweepersoons&p=2&templateid=1452"
        #     ]
        # },
        # "rugs": {
        #     "urls": [
        #         "https://www.fonq.nl/producten/categorie-vloerkleden/vorm-rechthoekig/",
        #         "https://www.fonq.nl/producten/categorie-vloerkleden/?ms_fk_vorm=Rechthoekig&p=2&templateid=339",
        #         "https://www.fonq.nl/producten/categorie-vloerkleden/?ms_fk_vorm=Rechthoekig&p=3&templateid=339",
        #         "https://www.fonq.nl/producten/categorie-vloerkleden/?ms_fk_vorm=Rechthoekig&p=4&templateid=339",
        #         "https://www.fonq.nl/producten/categorie-vloerkleden/?ms_fk_vorm=Rechthoekig&p=5&templateid=339",
        #         "https://www.fonq.nl/producten/categorie-vloerkleden/?ms_fk_vorm=Rechthoekig&p=6&templateid=339",
        #         "https://www.fonq.nl/producten/categorie-vloerkleden/?ms_fk_vorm=Rechthoekig&p=7&templateid=339",
        #         "https://www.fonq.nl/producten/categorie-vloerkleden/?ms_fk_vorm=Rechthoekig&p=8&templateid=339",
        #         "https://www.fonq.nl/producten/categorie-vloerkleden/?ms_fk_vorm=Rechthoekig&p=9&templateid=339",
        #         "https://www.fonq.nl/producten/categorie-vloerkleden/?ms_fk_vorm=Rechthoekig&p=10&templateid=339",
        #         "https://www.fonq.nl/producten/categorie-vloerkleden/?ms_fk_vorm=Rechthoekig&p=11&templateid=339",
        #         "https://www.fonq.nl/producten/categorie-vloerkleden/?ms_fk_vorm=Rechthoekig&p=12&templateid=339",
        #         "https://www.fonq.nl/producten/categorie-vloerkleden/?ms_fk_vorm=Rechthoekig&p=13&templateid=339",
        #         "https://www.fonq.nl/producten/categorie-vloerkleden/?ms_fk_vorm=Rechthoekig&p=14&templateid=339",
        #         "https://www.fonq.nl/producten/categorie-vloerkleden/?ms_fk_vorm=Rechthoekig&p=15&templateid=339",
        #         "https://www.fonq.nl/producten/categorie-vloerkleden/?ms_fk_vorm=Rechthoekig&p=16&templateid=339",
        #         "https://www.fonq.nl/producten/categorie-vloerkleden/?ms_fk_vorm=Rechthoekig&p=17&templateid=339",
        #         "https://www.fonq.nl/producten/categorie-vloerkleden/?ms_fk_vorm=Rechthoekig&p=18&templateid=339",
        #         "https://www.fonq.nl/producten/categorie-vloerkleden/?ms_fk_vorm=Rechthoekig&p=19&templateid=339",
        #     ]
        # },
        # "pendant_lights": {
        #     "urls": [
        #         "https://www.fonq.nl/producten/categorie-hanglampen/",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=2",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=3",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=4",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=5",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=6",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=7",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=8",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=9",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=10",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=11",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=12",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=13",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=14",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=15",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=16",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=17",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=18",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=19",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=20",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=21",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=22",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=23",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=24",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=25",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=26",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=27",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=28",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=29",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=30",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=31",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=32",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=33",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=34",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=35",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=36",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=37",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=38",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=39",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=40",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=41",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=42",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=43",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=44",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=45",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=46",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=47",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=48",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=49",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=50",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=51",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=52",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=53",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=54",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=55",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=56",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=57",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=58",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=59",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=60",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=61",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=62",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=63",
        #         "https://www.fonq.nl/producten/categorie-hanglampen/?p=64",
        #
        #     ]
        # },
        # "wall_lights": {
        #     "urls": [
        #         "https://www.fonq.nl/producten/categorie-wandlampen/",
        #         "https://www.fonq.nl/producten/categorie-wandlampen/?p=2",
        #         "https://www.fonq.nl/producten/categorie-wandlampen/?p=3",
        #         "https://www.fonq.nl/producten/categorie-wandlampen/?p=4",
        #         "https://www.fonq.nl/producten/categorie-wandlampen/?p=5",
        #         "https://www.fonq.nl/producten/categorie-wandlampen/?p=6",
        #         "https://www.fonq.nl/producten/categorie-wandlampen/?p=7",
        #         "https://www.fonq.nl/producten/categorie-wandlampen/?p=8",
        #         "https://www.fonq.nl/producten/categorie-wandlampen/?p=9",
        #         "https://www.fonq.nl/producten/categorie-wandlampen/?p=10",
        #         "https://www.fonq.nl/producten/categorie-wandlampen/?p=11",
        #         "https://www.fonq.nl/producten/categorie-wandlampen/?p=12",
        #         "https://www.fonq.nl/producten/categorie-wandlampen/?p=13",
        #         "https://www.fonq.nl/producten/categorie-wandlampen/?p=14",
        #         "https://www.fonq.nl/producten/categorie-wandlampen/?p=15",
        #         "https://www.fonq.nl/producten/categorie-wandlampen/?p=16",
        #     ]
        # },
        # "floor_lights": {
        #     "urls": [
        #         "https://www.fonq.nl/producten/categorie-vloerlampen/",
        #         "https://www.fonq.nl/producten/categorie-vloerlampen/?p=2",
        #         "https://www.fonq.nl/producten/categorie-vloerlampen/?p=3",
        #         "https://www.fonq.nl/producten/categorie-vloerlampen/?p=4",
        #         "https://www.fonq.nl/producten/categorie-vloerlampen/?p=5",
        #         "https://www.fonq.nl/producten/categorie-vloerlampen/?p=6",
        #         "https://www.fonq.nl/producten/categorie-vloerlampen/?p=7",
        #         "https://www.fonq.nl/producten/categorie-vloerlampen/?p=8",
        #         "https://www.fonq.nl/producten/categorie-vloerlampen/?p=9",
        #         "https://www.fonq.nl/producten/categorie-vloerlampen/?p=10",
        #         "https://www.fonq.nl/producten/categorie-vloerlampen/?p=11",
        #         "https://www.fonq.nl/producten/categorie-vloerlampen/?p=12",
        #         "https://www.fonq.nl/producten/categorie-vloerlampen/?p=13",
        #         "https://www.fonq.nl/producten/categorie-vloerlampen/?p=14",
        #         "https://www.fonq.nl/producten/categorie-vloerlampen/?p=15",
        #         "https://www.fonq.nl/producten/categorie-vloerlampen/?p=16",
        #         "https://www.fonq.nl/producten/categorie-vloerlampen/?p=17",
        #         "https://www.fonq.nl/producten/categorie-vloerlampen/?p=18",
        #         "https://www.fonq.nl/producten/categorie-vloerlampen/?p=19",
        #         "https://www.fonq.nl/producten/categorie-vloerlampen/?p=20",
        #         "https://www.fonq.nl/producten/categorie-vloerlampen/?p=21",
        #         "https://www.fonq.nl/producten/categorie-vloerlampen/?p=22",
        #         "https://www.fonq.nl/producten/categorie-vloerlampen/?p=23",
        #         "https://www.fonq.nl/producten/categorie-vloerlampen/?p=24",
        #         "https://www.fonq.nl/producten/categorie-vloerlampen/?p=25",
        #         "https://www.fonq.nl/producten/categorie-vloerlampen/?p=26",
        #
        #     ]
        # },
        # "table_lights": {
        #     "urls": [
        #         "https://www.fonq.nl/producten/categorie-tafellampen/",
        #         "https://www.fonq.nl/producten/categorie-tafellampen/?p=2",
        #         "https://www.fonq.nl/producten/categorie-tafellampen/?p=3",
        #         "https://www.fonq.nl/producten/categorie-tafellampen/?p=4",
        #         "https://www.fonq.nl/producten/categorie-tafellampen/?p=5",
        #         "https://www.fonq.nl/producten/categorie-tafellampen/?p=6",
        #         "https://www.fonq.nl/producten/categorie-tafellampen/?p=7",
        #         "https://www.fonq.nl/producten/categorie-tafellampen/?p=8",
        #         "https://www.fonq.nl/producten/categorie-tafellampen/?p=9",
        #         "https://www.fonq.nl/producten/categorie-tafellampen/?p=10",
        #         "https://www.fonq.nl/producten/categorie-tafellampen/?p=11",
        #         "https://www.fonq.nl/producten/categorie-tafellampen/?p=12",
        #         "https://www.fonq.nl/producten/categorie-tafellampen/?p=13",
        #         "https://www.fonq.nl/producten/categorie-tafellampen/?p=14",
        #         "https://www.fonq.nl/producten/categorie-tafellampen/?p=15",
        #         "https://www.fonq.nl/producten/categorie-tafellampen/?p=16",
        #         "https://www.fonq.nl/producten/categorie-tafellampen/?p=17",
        #         "https://www.fonq.nl/producten/categorie-tafellampen/?p=18",
        #         "https://www.fonq.nl/producten/categorie-tafellampen/?p=19",
        #         "https://www.fonq.nl/producten/categorie-tafellampen/?p=20",
        #         "https://www.fonq.nl/producten/categorie-tafellampen/?p=21",
        #         "https://www.fonq.nl/producten/categorie-tafellampen/?p=22",
        #         "https://www.fonq.nl/producten/categorie-tafellampen/?p=23",
        #         "https://www.fonq.nl/producten/categorie-tafellampen/?p=24",
        #         "https://www.fonq.nl/producten/categorie-tafellampen/?p=25",
        #         "https://www.fonq.nl/producten/categorie-tafellampen/?p=26",
        #         "https://www.fonq.nl/producten/categorie-tafellampen/?p=27",
        #         "https://www.fonq.nl/producten/categorie-tafellampen/?p=28",
        #         "https://www.fonq.nl/producten/categorie-tafellampen/?p=29",
        #
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

        products_ = soup.find_all("div", class_="product-new")

        for item in products_:
            try:
                detail_link = item.find("a", class_="link-muted")
                detail_url = detail_link["href"]
                title = detail_link.get_text()

                price = item.find("div", class_="product-price").get_text().strip().replace('€ ', '')

                product_id = detail_url.split('/')[-2]

                product_item = {
                    "product_id": product_id,
                    "detail_url": PREFIX_URL + detail_url,
                    "title": title.strip(),
                    "price": price,
                    "category": category,
                    "competitor": "fonq"
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
        tables = soup.find_all("table", class_="table-specs")

        print(product_item["detail_url"])
        print(f"{product_item['product_id']} - tables: {len(tables)}")

        for t in tables:
            trs = t.find_all('tr')
            for tr in trs:
                tds = tr.find_all('td')
                label = tds[0].get_text().strip()
                value = tds[1].get_text().strip()
                product_item[label] = value
                print(f"{label} - {value}")

    except Exception as e:
        print(f"Exception parsing technical specification detail for product id: {product_item['product_id']} - {e}")

    return product_item

def save_final_output_file(products, category):
    output_file = open(f'output/fonq_{category}.json', 'w')
    json.dump(products, output_file)
    output_file.close()



driver = webdriver.PhantomJS() # or add to your PATH

start_time = time.time()


for category, config in CATEGORIES_URL.items():
    print(f"====== {category} ======")

    products = get_products_from_listing_page(category, config)

    output = []

    print(f"Found: {len(products)} products")
    for product_item in products:
        product_start = time.time()
        # get detail url
        driver.get(product_item["detail_url"])

        detail_page_soup = BeautifulSoup(driver.page_source, 'html.parser')

        item = parse_detail_specification(product_item, detail_page_soup)
        output.append(item)

        product_end = time.time()
        print(f"product scraped & saved in {product_end-product_start} seconds")
    save_final_output_file(output, category)
    print(f"====== {category} ======")

end_time = time.time()
difference = end_time - start_time
print(f'time of processing: {difference}')