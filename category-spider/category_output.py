import logging
from dao import FileStorageClient, DataStorageClient
import json

logger = logging.getLogger('category-output')
logger.setLevel(logging.INFO)


file_client = FileStorageClient()
data_client = DataStorageClient()

TABLE_NAMES = {
    "made-dev-competitor-analysis": "competitor_analysis_overall_dev",
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

        data_client.store_items(TABLE_NAMES[bucket_name], data)

    return event
