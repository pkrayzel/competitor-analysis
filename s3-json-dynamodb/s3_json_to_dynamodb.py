import logging
from dao import FileStorageClient, DataStorageClient
from common import ConverterOverall
import json

logger = logging.getLogger('category-output')
logger.setLevel(logging.INFO)


file_client = FileStorageClient()
data_client = DataStorageClient()

S3_TO_DYNAMO_CONFIGURATION = {
    "made-dev-competitor-analysis": ConverterOverall("competitor_analysis_overall_dev")
}


def handler(event, context):
    logger.info(f"event: {event}")

    for record in event.get('Records', []):
        s3 = record['s3']

        bucket_name = s3['bucket']['name']
        key = s3['object']['key']
        file_content = file_client.get(
            bucket_name=bucket_name,
            file_key=key
        )

        data = json.load(file_content)

        converter = S3_TO_DYNAMO_CONFIGURATION.get(bucket_name)

        if converter:
            data_client.store_items(items=data,
                                    converter=converter)
        else:
            logger.warning(f"Received file: {key} in bucket: {bucket_name} which is not configured. Ignoring.")

    return event
