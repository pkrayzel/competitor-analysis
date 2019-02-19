from bs4 import BeautifulSoup
import requests
import time
import json

PREFIX_URL = "https://www.westwingnow.nl"

CATEGORIES_URL = {
        # "2_seat_sofas": {
        #     "urls": [
        #         "https://www.westwingnow.nl/2-zitsbanken/?sort=score_alternative_ranking_1&order=desc"
        #     ]
        # },
        # "3_seat_sofas": {
        #     "urls": [
        #         "https://www.westwingnow.nl/3-zitsbanken/?sort=score_alternative_ranking_1&order=desc"
        #     ]
        # },
        # "corner_sofa": {
        #     "urls": [
        #         "https://www.westwingnow.nl/hoekbanken/?sort=score_alternative_ranking_1&order=desc"
        #     ]
        # },
        # "sofa_beds": {
        #     "urls": [
        #         "https://www.westwingnow.nl/slaapbanken/?sort=score_alternative_ranking_1&order=desc"
        #     ]
        # },
        # "arm_chairs": {
        #     "urls": [
        #         "https://www.westwingnow.nl/fauteuils/?sort=score_alternative_ranking_1&order=desc",
        #         "https://www.westwingnow.nl/fauteuils/?sort=score_alternative_ranking_1&order=desc&page=2",
        #         "https://www.westwingnow.nl/fauteuils/?sort=score_alternative_ranking_1&order=desc&page=3"
        #     ]
        # },
        # "dining_chairs": {
        #     "urls": [
        #         "https://www.westwingnow.nl/stoelen/?sort=score_alternative_ranking_1&order=desc",
        #         "https://www.westwingnow.nl/stoelen/?sort=score_alternative_ranking_1&order=desc&page=2",
        #         "https://www.westwingnow.nl/stoelen/?sort=score_alternative_ranking_1&order=desc&page=3",
        #         "https://www.westwingnow.nl/stoelen/?sort=score_alternative_ranking_1&order=desc&page=4"
        #     ]
        # },
        "beds": {
            "urls": [
                "https://www.westwingnow.nl/bedden/?sort=score_alternative_ranking_1&order=desc&facet_sleeper_dim=140+x+200+cm",
                "https://www.westwingnow.nl/bedden/?sort=score_alternative_ranking_1&order=desc&facet_sleeper_dim=160+x+200+cm",
                "https://www.westwingnow.nl/bedden/?sort=score_alternative_ranking_1&order=desc&facet_sleeper_dim=180+x+200+cm"
            ]
        },
        "rugs": {
            "urls": [
                "https://www.westwingnow.nl/rechthoekige-vloerkleden/?sort=score_alternative_ranking_1&order=desc",
                "https://www.westwingnow.nl/rechthoekige-vloerkleden/?sort=score_alternative_ranking_1&order=desc&page=2",
                "https://www.westwingnow.nl/rechthoekige-vloerkleden/?sort=score_alternative_ranking_1&order=desc&page=3",
                "https://www.westwingnow.nl/rechthoekige-vloerkleden/?sort=score_alternative_ranking_1&order=desc&page=4",
                "https://www.westwingnow.nl/ronde-vloerkleden/?sort=score_alternative_ranking_1&order=desc",
                "https://www.westwingnow.nl/lopers/?sort=score_alternative_ranking_1&order=desc",
                "https://www.westwingnow.nl/lopers/?sort=score_alternative_ranking_1&order=desc&page=2",
                "https://www.westwingnow.nl/schapenvachten-en-koeienhuiden/?sort=score_alternative_ranking_1&order=desc"
            ]
        },
        "pendant_lights": {
            "urls": [
                "https://www.westwingnow.nl/draadlampen/?sort=score_alternative_ranking_1&order=desc",
                "https://www.westwingnow.nl/draadlampen/?sort=score_alternative_ranking_1&order=desc&page=2",
                "https://www.westwingnow.nl/draadlampen/?sort=score_alternative_ranking_1&order=desc&page=3",
                "https://www.westwingnow.nl/draadlampen/?sort=score_alternative_ranking_1&order=desc&page=4",
                "https://www.westwingnow.nl/draadlampen/?sort=score_alternative_ranking_1&order=desc&page=5",
                "https://www.westwingnow.nl/draadlampen/?sort=score_alternative_ranking_1&order=desc&page=6",
                "https://www.westwingnow.nl/draadlampen/?sort=score_alternative_ranking_1&order=desc&page=7",
                "https://www.westwingnow.nl/decoratieve-plafondlampen/?sort=score_alternative_ranking_1&order=desc"
            ]
        },
        "wall_lights": {
            "urls": [
                "https://www.westwingnow.nl/wandlampen/?sort=score_alternative_ranking_1&order=desc",
                "https://www.westwingnow.nl/wandlampen/?sort=score_alternative_ranking_1&order=desc&page=2",
                "https://www.westwingnow.nl/wandlampen/?sort=score_alternative_ranking_1&order=desc&page=3"
            ]
        },
        "floor_lights": {
            "urls": [
                "https://www.westwingnow.nl/staande-lampen/?sort=score_alternative_ranking_1&order=desc",
                "https://www.westwingnow.nl/staande-lampen/?sort=score_alternative_ranking_1&order=desc&page=2",
                "https://www.westwingnow.nl/staande-lampen/?sort=score_alternative_ranking_1&order=desc",
                "https://www.westwingnow.nl/staande-lampen/?sort=score_alternative_ranking_1&order=desc",
            ]
        },
        "table_lights": {
            "urls": [
                "https://www.westwingnow.nl/tafellampen/?sort=score_alternative_ranking_1&order=desc",
                "https://www.westwingnow.nl/tafellampen/?sort=score_alternative_ranking_1&order=desc&page=2",
                "https://www.westwingnow.nl/tafellampen/?sort=score_alternative_ranking_1&order=desc&page=3",
                "https://www.westwingnow.nl/tafellampen/?sort=score_alternative_ranking_1&order=desc&page=4",
                "https://www.westwingnow.nl/tafellampen/?sort=score_alternative_ranking_1&order=desc&page=5"
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

        products_ = soup.find_all("div", class_="blockProductGrid__item")

        for item in products_:
            try:
                detail_link = item.find("a", class_="blockProduct__link")
                detail_url = detail_link["href"]

                title = item.find("p", class_="blockProduct__name")
                product_id = detail_url.split('simple=')[-1]

                price_box = item.find("span", class_="blockProduct__priceAmount")

                product_item = {
                    "product_id": product_id,
                    "detail_url": PREFIX_URL + detail_url,
                    "title": title.get_text().strip(),
                    "price": price_box.get_text().strip(),
                    "category": category,
                    "competitor": "westwingnow"
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
        data_labels = soup.find_all("h4", class_="blockDetails__heading")
        data_values = soup.find_all("p", class_="blockDetails__text")

        for i in range(len(data_labels)):
            label = data_labels[i].get_text()
            value = data_values[i].get_text()
            product_item[label] = value

    except Exception as e:
        print(f"Exception parsing specification for product id {product_item['product_id']} - {e}")


def save_final_output_file(products, category):
    output_file = open(f'output/westwingnow_{category}.json', 'w')
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