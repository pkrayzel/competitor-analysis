import json
from collections import defaultdict
import os
import sys
from collections import defaultdict


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Path to the directory should be provided as an argument.")
        sys.exit(-1)

    file_name = sys.argv[1]

    files = os.listdir(file_name)

    results = defaultdict(lambda: {
        "products_count": 0,
        "product_details_count": 0,
        "top_quality": 0,
        "missing_data": 0
    })

    for f in files:
        if "nl_fonq" not in f:
            continue

        with open(file_name+f, 'r') as data_file:

            data = json.load(data_file)

            results[data[0]["category"]]["product_details_count"] += len(data)

    for k, v in results.items():
        print(f"{k}: {v}")

    # results = defaultdict(lambda: {
    #     "product_links_count": 0,
    #     "products_count": 0
    # })
    #
    #
    #     print(f"Total amount of category-pages: {len(data)}")
    #
    #     for item in data:
    #         results[item["category"]]["product_links_count"] += item["product_links_count"]
    #         results[item["category"]]["products_count"] = item["products_count"]
    #
    # for key, value in results.items():
    #     print(f"{key}: {value}")