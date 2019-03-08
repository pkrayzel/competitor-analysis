import boto3
import logging
import math
import json

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

    BATCH_REQUEST_LIMIT = 25

    def __init__(self, endpoint_url=None):
        self.client = boto3.client('dynamodb', endpoint_url=endpoint_url)

    def store_items(self, items, converter, environment):
        logger.info(f"Number of items to store in table {converter.table_name}: {len(items)}")

        table_name = f"{converter.table_name}_{environment}"

        request_count = math.ceil(len(items) / DataStorageClient.BATCH_REQUEST_LIMIT)

        logger.info(f"Will be stored in following number of requests: {request_count}")
        for i in range(request_count):
            start = i * DataStorageClient.BATCH_REQUEST_LIMIT
            end = (i + 1) * DataStorageClient.BATCH_REQUEST_LIMIT

            items_page = items[start:end]
            logger.info(f"Sending page number {i} of items [{start}:{end}] to dynamodb...")
            self._store_items_batch(table_name, converter, items_page)
            logger.info("Successfully stored.")


    def _store_items_batch(self, table_name, converter, items):
        self.client.batch_write_item(
            RequestItems={
                table_name: converter.convert_json_items_to_put_requests(items)
            },
            ReturnConsumedCapacity='TOTAL',
            ReturnItemCollectionMetrics='SIZE'
        )


class QueueClient:

    def __init__(self, queue_name, endpoint_url=None):
        sqs = boto3.resource('sqs', endpoint_url=endpoint_url)
        self.queue = sqs.get_queue_by_name(QueueName=queue_name)

    def store_items(self, items):
        logger.info(f"Number of items to send to SQS queue: {len(items)}")

        for i, item in enumerate(items):
            logger.info(f"Sending item: {i+1}...")
            self.queue.send_message(
                DelaySeconds=1,
                MessageBody=json.dumps(item)
            )
