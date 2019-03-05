import time
from datetime import datetime


class Converter:

    def __init__(self, table_name):
        self.table_name = table_name

    def convert_json_items_to_put_requests(self, items):
        result = []
        for item in items:
            result.append(self.convert_json_item_to_put_request(item))
        return result

    def convert_json_item_to_put_request(self, item):
        dynamodb_item = {
            self.key_attribute_name(): Converter.convert_value(self.key_attribute_value(item)),
        }

        self.append_date_time_fields(dynamodb_item)

        for key, value in item.items():
            dynamodb_item[key] = Converter.convert_value(value)

        return {
            "PutRequest": {
                "Item": dynamodb_item
            }
        }

    def key_attribute_name(self):
        raise NotImplementedError("Must be implemented in subclasses.")

    def key_attribute_value(self, item):
        raise NotImplementedError("Must be implemented in subclasses.")

    def append_date_time_fields(self, dynamodb_item):
        date = datetime.utcnow()
        dynamodb_item["timestamp"] = Converter.convert_value(str(int(time.mktime(date.timetuple())) * 1000))
        dynamodb_item["date"] = Converter.convert_value(date.strftime("%Y-%m-%d"))
        dynamodb_item["time"] = Converter.convert_value(date.strftime("%H-%M-%S"))

    @staticmethod
    def convert_value(value):
        data_type = "S"

        if type(value) == int:
            data_type = "N"

        return {
            data_type: str(value)
        }


class ConverterOverall(Converter):

    def key_attribute_name(self):
        return "country_competitor_category"

    def key_attribute_value(self, item):
        return f"{item['country']}_{item['competitor']}_{item['category']}"
