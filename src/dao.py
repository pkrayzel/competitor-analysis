import boto3
import logging

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

    def store_items(self, items, converter, environment):
        logger.info(f"Number of items to store in table {converter.table_name}: {len(items)}")

        table_name = f"{converter.table_name}_{environment}"
        print(f"table name: {table_name}")
        response = self.client.batch_write_item(
            RequestItems={
                table_name: converter.convert_json_items_to_put_requests(items)
            },
            ReturnConsumedCapacity='TOTAL',
            ReturnItemCollectionMetrics='SIZE'
        )
        logger.info(f'DynamoDB response: {response}')
