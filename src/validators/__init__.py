from cerberus import Validator


category_spider_validator = Validator({
    "competitors": {
        "type": "list",
        "minlength": 1,
        "required": True,
        "schema": {
            "type": "dict",
            "schema": {
                "name": {
                    "type": "string",
                    "required": True
                },
                "country": {
                    "type": "string",
                    "required": True
                },
            }
        }
    },
})


product_pages_validator = Validator({
    "Records": {
        "type": "list",
        "minlength": 1,
        "maxlength": 1,
        "required": True,
        "schema": {
            "type": "dict",
            "schema": {
                "messageId": { "type": "string", "required": True },
                "receiptHandle": { "type": "string", "required": True },
                "body": { "type": "string", "required": True },
                "attributes": { "type": "dict", "required": True },
                "messageAttributes": { "type": "dict", "required": True },
                "md5OfBody": { "type": "string", "required": True },
                "eventSource": { "type": "string", "required": True },
                "eventSourceARN": { "type": "string", "required": True },
                "awsRegion": { "type": "string", "required": True },
            }
        }
    },
})


json_to_csv_validator = Validator({
    "date": {"type": "string", "required": True}
})
