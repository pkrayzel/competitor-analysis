import json
import sys
from collections import defaultdict


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Path to the json file should be provided as an argument.")
        sys.exit(-1)

    file_name = sys.argv[1]

    results = defaultdict(lambda: {
        "product_links_count": 0,
        "products_count": 0
    })

    with open(file_name, 'r') as f:
        data = json.load(f)
        for item in data:
            results[item["category"]]["product_links_count"] += item["product_links_count"]
            results[item["category"]]["products_count"] = item["products_count"]

    for key, value in results.items():
        print(f"{key}: {value}")