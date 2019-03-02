import logging
from dao import StorageClient
import json

logger = logging.getLogger('category-output')
logger.setLevel(logging.INFO)


client = StorageClient()


def handler(event, context):
    logger.info(f"event: {event}")

    for record in event.get('Records', []):
        s3 = record['s3']

        bucket_name = s3['bucket']['name']
        key = s3['object']['key']
        content = client.get(
            bucket_name=bucket_name,
            file_key=key
        )

        data = json.load(content)

        logger.info(data)
        logger.info(f"Number of items: {len(data)}")

    return event