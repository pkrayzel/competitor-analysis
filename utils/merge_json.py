import os

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

            for dir in dirs:

                for subdir, dirs, files in os.walk(start_dir + "/" + dir):

                    print(f"{dir} - number of files: {len(files)}")
                    # for filename in files:
                    #     print(filename)

if __name__ == "__main__":
    main()
