import logging
import json
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class FileStorageClient:

    def __init__(self, client, bucket_name):
        self.client = client
        self.bucket_name = bucket_name

    def upload_local_file(self, file_name):
        s3_file_key = file_name.replace('_', '/')

        logging.info(f"Opening file {file_name}.")
        file_content = open(file_name, 'rb').read()

        logging.info(f"Saving file in s3 bucket with file_key s3://{self.bucket_name}/{s3_file_key}.")
        self._upload(file_key=s3_file_key, file_content=file_content)

    def get(self, file_key):
        logger.info(f'Getting file content for the file: {file_key} from the bucket: {self.bucket_name}')
        response = self.client.get_object(
            Bucket=self.bucket_name,
            Key=file_key
        )
        return response['Body']

    def _upload(self, file_key, file_content):
        logger.info(f'Uploading file {file_key} into bucket {self.bucket_name}...')
        self.client.put_object(
            Bucket=self.bucket_name,
            Key=file_key,
            Body=file_content
        )

    def download_directory(self, directory_prefix, local_directory):
        os.system(f"mkdir {local_directory}")
        os.system(f"aws s3 sync s3://{self.bucket_name}/{directory_prefix} {local_directory}")


class QueueClient:

    def __init__(self, resource, queue_name):
        self.resource = resource
        self.queue_name = queue_name
        self.queue = self.resource.get_queue_by_name(QueueName=self.queue_name)

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
        logger.info(f"Deleting consumed message from SQS queue: {self.queue_name}")
        self.resource.meta.client.delete_message(
            QueueUrl=self.queue.url,
            ReceiptHandle=receipt_handle
        )

    def store_items(self, items):
        logger.debug(f"Number of items to send to SQS queue {self.queue_name} - {len(items)}")

        for i, item in enumerate(items):
            logger.info(f"Sending item: {i+1}...")
            self.queue.send_message(
                DelaySeconds=1,
                MessageBody=json.dumps(item)
            )
