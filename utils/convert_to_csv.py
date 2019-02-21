import os
import json
import csv


COMPETITORS_PRODUCT_PER_FILE = [
    "bolia",
    # "fonq",

]


def return_all_products_for_competitor(competitor):
    pass

def main():
    for competitor in COMPETITORS_PRODUCT_PER_FILE:
        print("------------------")
        print(f"competitor: {competitor}")
        print("------------------")
        start_dir = f"../{competitor}/output/"

        for subdir, dirs, files in os.walk(start_dir):

            for f in files:

                header_keys = set()

                if f.startswith("bolia_"):
                    path = f"{start_dir}{f}"
                    with open(path) as category_file:
                        category_data = json.load(category_file)

                        # we'll go through each row in category data file
                        for item in category_data:
                            # we will first get keys and put them into header set
                            # for csv we want to build full list of unique keys
                            for header_key in item.keys():
                                header_keys.add(header_key.lower())

                        print(f"{f} - {header_keys}")

                        output_filename = f.replace('.json', '.csv')

                        with open(output_filename, 'w', newline='') as output_file:
                            writer = csv.DictWriter(output_file, fieldnames=header_keys)
                            writer.writeheader()

                            for item in category_data:
                                writer.writerow(item)

                # products_for_category = []
                #
                # for filename in files:
                #     full_path = f"{category_directory}{filename}"
                #
                    # read each product file
                    # with open(full_path) as f:
                    #     product = json.load(f)
                    #     products_for_category.append(product)
                #
                # output_filename = f"{start_dir}/{competitor}_{directory}.json"
                # write list of products for category to output file
                # with open(output_filename, 'w') as output_file:
                #     json.dump(products_for_category, output_file, indent=4)






if __name__ == "__main__":
    main()
