import json
import logging
import inject
import time

from spiders.category_info import run_category_info
from spiders.product_details import run_product_details


class CategoryInfoHandler:

    @inject.params(file_storage_client='file_storage_client')
    @inject.params(queue_client='queue_client')
    def __init__(self, file_storage_client, queue_client):
        self.file_storage_client = file_storage_client
        self.queue_client = queue_client

    def __call__(self, competitor):
        start_time = time.time()
        logging.info(f"Category information handler is running for competitor: {competitor}")

        # TODO: redesign this
        # - where to get this config from?
        # - how to run multiple competitors?
        # - how to run only some categories for one competitor?
        file_name = run_category_info(competitor)
        logging.info(f"Successfuly scraped and generated file: {file_name}.")

        try:
            self.file_storage_client.upload_local_file(file_name)

            with open(file_name, 'r') as f:
                logging.info(f"Parsing file content to json...")
                data = json.load(f)

            logging.info(f"Sending {len(data)} items to SQS one by one...")
            self.queue_client.store_items(items=data)

        except Exception as e:
            logging.error(f"Error happened during processing file: {file_name} - {e}")
        end_time = time.time()
        logging.info(f"CategoryInfo handler finished processing in: {end_time-start_time} seconds")


class ProductDetailsHandler:

    @inject.params(file_storage_client='file_storage_client')
    @inject.params(queue_client='queue_client')
    def __init__(self, file_storage_client, queue_client):
        self.file_storage_client = file_storage_client
        self.queue_client = queue_client

    def __call__(self):
        logging.info('Starting product details handler')

        no_message_counter = 0
        max_not_found_counter = 10

        while no_message_counter < max_not_found_counter:
            logging.info('Getting a message from SQS... ')
            message, receipt_handle = self.queue_client.receive_message()

            if message:
                logging.info("Received a new SQS message - will process it in a bit.")

                no_message_counter = 0

                logging.info("Parsing message body to json.")
                item = json.loads(message)

                logging.info(f'Starting scraping for competitor {item["competitor"]} and category {item["category"]}.')

                file_name = run_product_details(item)

                self.file_storage_client.upload_local_file(file_name)

                logging.info("Successfuly consumed SQS message - removing it from SQS...")
                self.queue_client.delete_message(receipt_handle)

            else:
                no_message_counter += 1
                logging.info(f"No new SQS message found - sleeping for 5 seconds and increasing counter ({no_message_counter})")
                time.sleep(5)

        logging.info(f"No new messages were found {max_not_found_counter} times in a row. Exiting the job now.")


class ProductDetailsConversionHandler:

    pass