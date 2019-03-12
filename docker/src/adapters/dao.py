import boto3
import logging
import math
import json
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class FileStorageClient:

    def __init__(self, endpoint_url=None):
        self.resource = boto3.resource('s3', endpoint_url=endpoint_url)

    def get(self, bucket_name, file_key):
        logger.info(f'Getting file content for the file: {file_key} from the bucket: {bucket_name}')
        response = self.resource.meta.client.get_object(
            Bucket=bucket_name,
            Key=file_key
        )
        return response['Body']

    def upload(self, bucket_name, file_key, file_content):
        logger.info(f'Uploading file {file_key} into bucket {bucket_name}...')
        self.resource.meta.client.put_object(
            Bucket=bucket_name,
            Key=file_key,
            Body=file_content
        )

    def download_directory(self, bucket_name, directory_prefix, local_directory):
        os.system(f"mkdir {local_directory}")
        os.system(f"aws s3 sync s3://{bucket_name}/{directory_prefix} {local_directory}")


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
        self.sqs = boto3.resource('sqs', endpoint_url=endpoint_url)
        self.queue_name = queue_name
        self.queue = self.sqs.get_queue_by_name(QueueName=self.queue_name)

    def receive_message(self):
        logger.info(f"Receiving messages from SQS queue")
        messages = self.queue.receive_messages(
            AttributeNames=['SentTimestamp'],
            MaxNumberOfMessages=1,
            MessageAttributeNames=['All'],
            VisibilityTimeout=900,
            WaitTimeSeconds=3
        )
        if messages:
            return messages[0].body, messages[0].receipt_handle
        else:
            return None, None

    def delete_message(self, receipt_handle):
        logger.info(f"Deleting consumed message from SQS queue")
        self.sqs.meta.client.delete_message(
            QueueUrl=self.queue.url,
            ReceiptHandle=receipt_handle
        )

    def store_items(self, items):
        logger.info(f"Number of items to send to SQS queue: {len(items)}")

        for i, item in enumerate(items):
            logger.info(f"Sending item: {i+1}...")
            self.queue.send_message(
                DelaySeconds=1,
                MessageBody=json.dumps(item)
            )
