from infrastructure import bootstrap
from services.handlers import CategoryInfoHandler, CategoryInfoSendToQueueHandler


def main():
    bootstrap.bootstrap()

    # scraping handler
    handler = CategoryInfoHandler()
    file_name = handler({
        "country": "nl",
        "name": "flinders"
    })

    # send messages to SQS
    handler = CategoryInfoSendToQueueHandler()
    handler(file_name)


if __name__ == "__main__":
    main()
