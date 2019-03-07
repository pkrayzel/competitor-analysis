import os
import logging
import aws_lambda_logging
from dao import FileStorageClient, DataStorageClient
from converter import ConverterOverall
import json

aws_lambda_logging.setup(level='INFO', boto_level='CRITICAL')
logging.getLogger('urllib3').setLevel(logging.CRITICAL)


file_client = FileStorageClient()
data_client = DataStorageClient()

S3_TO_DYNAMO_CONFIGURATION = {
    "category-overall-info": ConverterOverall("competitor_category_overall_info")
}


def get_converter(key):
    for key_prefix, value in S3_TO_DYNAMO_CONFIGURATION.items():
        if key.startswith(key_prefix):
            return value


def handler(event, context):
    environment = os.getenv('ENV', 'dev')

    if "Records" not in event:
        logging.error("Wrong input event - expecting 'Records' with S3 notification event.")
        return { "result": "error", "message": "wrong input data" }

    logging.info(f"event: {event}")

    for record in event['Records']:
        s3 = record['s3']

        bucket_name = s3['bucket']['name']

        key = s3['object']['key']
        file_content = file_client.get(
            bucket_name=bucket_name,
            file_key=key
        )

        data = json.load(file_content)

        converter = get_converter(key)

        if converter:
            data_client.store_items(items=data,
                                    converter=converter,
                                    environment=environment)
        else:
            logging.warning(f"Received file: {key} in bucket: {bucket_name} which is not configured. Ignoring.")

    return event
