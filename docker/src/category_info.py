from infrastructure import bootstrap
from services.handlers import CategoryInfoHandler


def main():
    bootstrap.bootstrap()

    handler = CategoryInfoHandler()
    handler({
        "country": "nl",
        "name": "flinders"
    })


if __name__ == "__main__":
    main()
