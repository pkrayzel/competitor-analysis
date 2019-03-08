def handler(event, context):
    if "Records" not in event:
        print("Wrong input event - expecting 'Records' with DynamoDB stream event.")
        return {"result": "error", "message": "wrong input data"}

    items = event["Records"]

    if len(items) > 1:
        print("Too many records in input event - expecting just one record.")
        return {"result": "error", "message": "wrong input data - too many records"}

    item = items[0]["dynamodb"]["NewImage"]["country_competitor_category_page_number"]["S"]
    print(f"Received item with key: {item}")
