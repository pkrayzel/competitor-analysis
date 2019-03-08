import os
import logging
import aws_lambda_logging
from adapters.dao import FileStorageClient, QueueClient
import json

aws_lambda_logging.setup(level='INFO', boto_level='CRITICAL')
logging.getLogger('urllib3').setLevel(logging.CRITICAL)


def main(event):
    queue_name = os.getenv('QUEUE_NAME', 'competitor-analysis-products-queue-dev')

    file_client = FileStorageClient()
    queue_client = QueueClient(queue_name=queue_name)

    try:
        if "Records" not in event:
            logging.error("Wrong input event - expecting 'Records' with S3 notification event.")
            return {"result": "error", "message": "wrong input data"}

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

            queue_client.store_items(items=data)

        return {
            "result": "success"
        }

    except Exception as e:
        return {
            "result": "error",
            "error_message": f"{str(type(e).__name__)}: {str(e)}"
        }


def handler(event, context):
    return main(event)