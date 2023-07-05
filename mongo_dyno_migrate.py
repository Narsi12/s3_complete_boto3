import pymongo
import boto3
from decimal import Decimal

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["online_goods_delevery_db"]
mycol = mydb['app_addresssourcedestination']
data = mycol.find()

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('delivery')

def convert_float_values_to_strings(data):
    if isinstance(data, float):
        return str(data)
    elif isinstance(data, list):
        return [convert_float_values_to_strings(item) for item in data]
    elif isinstance(data, dict):
        return {key: convert_float_values_to_strings(value) for key, value in data.items()}
    else:
        return data

for item in data:
    item = convert_float_values_to_strings(item)

    dynamodb_item = {
        'ID': str(item['_id']),  
        'userID': item['userID'],
        'order_type': item['order_type'],
        'qty': item['qty'],
        'temp_order_id': item['temp_order_id'],
        'date_info': item['date_info'].isoformat(),  
        'destination_info': item['destination_info'],
        'order_id': item['order_id'],
        'source_info': item['source_info'],
        'status': item['status'],
    }

    table.put_item(Item=dynamodb_item)

print("Data migration to DynamoDB completed.")

  