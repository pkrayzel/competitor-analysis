import boto3
import logging
from datetime import datetime
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class FileStorageClient:

    def __init__(self, endpoint_url=None):
        self.client = boto3.client('s3', endpoint_url=endpoint_url)

    def get(self, bucket_name, file_key):
        logger.info(f'Getting file content for the file: {file_key} from the bucket: {bucket_name}')
        response = self.client.get_object(
            Bucket=bucket_name,
            Key=file_key
        )
        return response['Body']


class DataStorageClient:

    def __init__(self, endpoint_url=None):
        self.client = boto3.client('dynamodb', endpoint_url=endpoint_url)

    def store_items(self, table_name, items):
        logger.info(f"Number of items to store in table {table_name}: {len(items)}")

        dynamo_items = []

        for item in items:
            dynamo_item = self._construct_overall_item_from_json(item)
            dynamo_items.append(dynamo_item)

        response = self.client.batch_write_item(
            RequestItems={
                table_name: dynamo_items
            },
            ReturnConsumedCapacity='TOTAL',
            ReturnItemCollectionMetrics='SIZE'
        )
        logger.info(f'DynamoDB response: {response}')

    def _construct_overall_item_from_json(self, item):
        key = f"{item['country']}_{item['competitor']}_{item['category']}"

        date = datetime.now()
        return {
            "PutRequest": {
                "Item": {
                    "country_competitor_category": {
                        "S": key,
                    },
                    "timestamp": {
                        "N": str(int(time.mktime(date.timetuple())) * 1000)
                    },
                    "country": {
                        "S": item['country']
                    },
                    "competitor": {
                        'S': item['competitor']
                    },
                    "category": {
                        'S': item['category']
                    },
                    "products_count": {
                        'N': str(item['products_count'])
                    },
                    "pages_count": {
                        'N': str(item['pages_count'])
                    },
                    "category_url": {
                        'S': item['category_url']
                    },
                    "date": {
                        'S': date.strftime("%Y-%m-%d")
                    },
                    "time": {
                        'S': date.strftime("%H:%M:%S")
                    },
                }
            }
        }
