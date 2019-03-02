import sys
import json
from jsonschema import validate


REQUIRED_SCHEMA = {
    "type": "object",
    "properties": {
        "page_url": {
            "type": "string"
        },
        "title": {
            "type": "string"
        },
        "price": {
            "type": "number"
        },
        "category_1": {
            "type": "string"
        },
        "category_2": {
            "type": "string"
        },
        "category_3": {
            "type": "string"
        },
        "breedte": {
            "type": "string"
        },
        "diepte": {
            "type": "string"
        },
        "hoogte": {
            "type": "string"
        },
        "productnummer": {
            "type": "string"
        },
        "kleur": {
            "type": "string"
        },
    },
}


def check_file(filename):
    with open(filename, 'r') as file_to_check:
        data = json.load(file_to_check)

    count = len(data)
    invalid_count = 0

    for item in data:
        try:
            validate(item, REQUIRED_SCHEMA)
        except Exception as e:
            invalid_count += 1
            pass

    print(f"Total amount of products: {count}")
    print(f"Invalid items: {invalid_count}")
    print(f"Quality ratio: {1-invalid_count/count}")

if __name__ == '__main__':
    args = sys.argv[1:]

    check_file(args[0])
