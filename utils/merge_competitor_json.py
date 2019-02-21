import os
import json

COMPETITORS = [
    "flinders",
    "ikea",
    "loods5",
    "sofa",
    "vtonen",
    "westwingnow",
    "bolia",
    "fonq"
]


def main():
    for competitor in COMPETITORS:
        # print("------------------")
        # print(f"competitor: {competitor}")
        # print("------------------")
        start_dir = f"../{competitor}/output"

        products_competitor = []

        for f in os.listdir(start_dir):

            full_path = f"{start_dir}/{f}"

            # read each competitor - category file
            with open(full_path, encoding="utf8", errors='ignore') as category_file:
                products = json.load(category_file)
                # print(f"file: {f} - {len(products)} records")

                products_competitor.extend(products)

        output_filename = f"json_output/{competitor}.json"
        # write list of products for category to output file
        with open(output_filename, 'w') as output_file:
            # print("------------")
            print(f"competitor: {competitor} \t\t {len(products_competitor)} records")

            json.dump(products_competitor, output_file, indent=4)

if __name__ == "__main__":
    main()
