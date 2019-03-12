from infrastructure import bootstrap

from services.handlers import ProductDetailsConversionHandler


def main(date_string):
    bootstrap.bootstrap()

    handler = ProductDetailsConversionHandler()
    handler(date_string)


if __name__ == "__main__":
    main("2019-03-12")

