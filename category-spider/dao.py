import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class StorageClient:

    def __init__(self, endpoint_url=None):
        self.client = boto3.client('s3', endpoint_url=endpoint_url)

    def get(self, bucket_name, file_key):
        logger.info(f'Downloading file content for the file: {file_key} from the bucket: {bucket_name}')
        response = self.client.get_object(
            Bucket=bucket_name,
            Key=file_key
        )
        return response['Body'].read()
