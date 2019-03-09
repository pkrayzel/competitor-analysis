import aws_lambda_logging
import csv
import os
import logging
import json

from competitors import find_competitor
from validators import json_to_csv_validator
from adapters.dao import FileStorageClient


aws_lambda_logging.setup(level='INFO', boto_level='CRITICAL')
logging.getLogger('urllib3').setLevel(logging.CRITICAL)

file_client = FileStorageClient()


def main(date_string):
    bucket_name = os.getenv('BUCKET_NAME', 'made-dev-competitor-analysis')
    directory = os.getenv('LOCAL_DIRECTORY', 'temp')

    logging.info(f"Getting all category-product-pages files from bucket: {bucket_name} for date: {date_string}")

    local_dir = f"{directory}/{date_string}"

    os.system(f"aws s3 sync s3://{bucket_name}/category-product-pages/{date_string}/ {local_dir}/")

    count = 0
    output_file_name = f"{directory}/output.csv"

    with open(output_file_name, 'w', newline='') as csv_file:

        writer = csv.DictWriter(csv_file,
                                fieldnames=["country", "competitor", "category", "price", "title"])
        writer.writeheader()

        for f in os.listdir(directory):

            if ".json" not in f:
                continue

            names = f.split("_")
            competitor = find_competitor(name=names[1], country=names[0])

            with open(local_dir + "/" + f, 'r') as json_file:
                logging.info(f"Opening a file: {f}")
                data = json.load(json_file)

                logging.info(f"File parsed to json, now writing file: {f} to csv...")
                count += len(data)
                for d in data:
                    item = competitor.convert_to_csv_item(d)
                    writer.writerow(item)

                logging.info(f"File {f} written to csv...")

    os.system(f"rm -rf {local_dir}")

    file_client.upload(bucket_name, f"product-data/{date_string}/data.csv", open(output_file_name, 'rb'))

    return {
        "result": "success",
        "records_count": count
    }


def handler(event, context):
    is_valid = json_to_csv_validator.validate(event)

    if not is_valid:
        return {
            "result": "error",
            "error_message": f"Wrong input - {json_to_csv_validator.errors}"
        }

    return main(event["date"])


if __name__ == "__main__":
    print(handler({"date": "2019-03-08"}, ""))