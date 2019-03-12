from infrastructure import bootstrap

from services.handlers import ProductDetailsHandler


def main():
    bootstrap.bootstrap()

    handler = ProductDetailsHandler()
    handler()


if __name__ == "__main__":
    main()
