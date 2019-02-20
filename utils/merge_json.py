import os
import json

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
        start_dir = f"../{competitor}/output"

        for subdir, dirs, files in os.walk(start_dir):

            for directory in dirs:
                category_directory = f"{start_dir}/{directory}/"

                for subdir, dirs, files in os.walk(category_directory):

                    print(f"{category_directory} - number of files: {len(files)}")

                    products_for_category = []

                    for filename in files:
                        full_path = f"{category_directory}{filename}"

                        # read each product file
                        with open(full_path) as f:
                            product = json.load(f)
                            products_for_category.append(product)

                    output_filename = f"{start_dir}/{competitor}_{directory}.json"
                    # write list of products for category to output file
                    with open(output_filename, 'w') as output_file:
                        json.dump(products_for_category, output_file, indent=4)






if __name__ == "__main__":
    main()
