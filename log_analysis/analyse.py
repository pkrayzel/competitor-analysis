from collections import defaultdict


def extract_value(text, search_text):
    if search_text in text:
        start = text.find(search_text)
        end = text.find(",", start)
        return int(text[start + len(search_text):end])
    return 0


data = open('product_pages_all.txt', 'r')

lines = data.readlines()

results = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict())))

competitor, country, category, page_number = "", "", "", ""

for i, line in enumerate(lines):

    # START line - skip
    if i % 5 == 0:
        continue

    if i % 5 == 1:
        info = line.split("Running product pages scraping for ")[1].replace('."}', '').split(',')

        competitor = info[0].split(':')[1].strip().replace('\n', '')
        country = info[1].split(':')[1].strip().replace('\n', '')
        category = info[2].split(':')[1].strip().replace('\n', '')
        page_number = info[3].split(':')[1].strip().replace('\n', '')

    if i % 5 == 2:
        info = line.split("Total scraping time: ")[1].replace(' seconds"}', '')
        results[competitor][category][page_number]["scraping_time"] = info

    if i % 5 == 3:
        info = line.split("Dumping Scrapy stats:")[1].replace('\n', '')
        results[competitor][category][page_number]["retry_count"] = extract_value(
            info, "'retry/count': "
        )
        results[competitor][category][page_number]["ignored_count"] = extract_value(
            info, "'httperror/response_ignored_count': "
        )
        results[competitor][category][page_number]["403_count"] = extract_value(
            info, "'retry/reason_count/403 Forbidden': "
        )

    if i % 5 == 4:
        info = line.split("Duration")
        results[competitor][category][page_number]["duration"] = float(info[1].replace(' ms\tBilled', '').strip().replace(': ', ''))
        results[competitor][category][page_number]["billed_duration"] = float(info[2].split('ms')[0].strip().replace(': ', ''))
        results[competitor][category][page_number]["memory"] = info[2].split('Max Memory Used: ')[1]

for competitor, value in results.items():
    for category, category_value in value.items():
        for page_number, pn_value in category_value.items():
            print(f"{competitor} - {category} - {page_number}")
            print("------------------------------------------")

            for m, val in pn_value.items():
                print(f"{m}: {val}")
