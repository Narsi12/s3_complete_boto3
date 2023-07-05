import pymongo
import boto3
from decimal import Decimal

# MongoDB configuration
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["online_goods_delivery_db"]

# DynamoDB configuration
dynamodb = boto3.resource('dynamodb')
table_name_prefix = 'delivery_'

def convert_float_values_to_strings(data):
    if isinstance(data, float):
        return str(data)
    elif isinstance(data, list):
        return [convert_float_values_to_strings(item) for item in data]
    elif isinstance(data, dict):
        return {key: convert_float_values_to_strings(value) for key, value in data.items()}
    else:
        return data

def migrate_collection(collection_name, field_mappings):
    collection = mongo_db[collection_name]
    dynamodb_table = dynamodb.Table(table_name_prefix + collection_name)

    data = collection.find()
    for item in data:
        item = convert_float_values_to_strings(item)

        dynamodb_item = {}
        for mongo_field, dynamodb_field in field_mappings.items():
            if mongo_field in item:
                value = item[mongo_field]
                if isinstance(value, pymongo.MongoBase):
                    value = value.isoformat()
                dynamodb_item[dynamodb_field] = value

        dynamodb_table.put_item(Item=dynamodb_item)

    print(f"Data migration for collection '{collection_name}' completed.")

# Field mappings for each collection
collection_field_mappings = {
    'app_addresssourcedestination': {
        '_id': 'ID',
        'userID': 'userID',
        'order_type': 'order_type',
        'qty': 'qty',
        'temp_order_id': 'temp_order_id',
        'date_info': 'date_info',
        'destination_info': 'destination_info',
        'order_id': 'order_id',
        'source_info': 'source_info',
        'status': 'status',
    },
    # Add more collections and their field mappings as needed
    'another_collection': {
        # Field mappings for 'another_collection'
    }
}

# Iterate through all collections in the MongoDB database
collection_names = mongo_db.list_collection_names()
for collection_name in collection_names:
    if collection_name in collection_field_mappings:
        field_mappings = collection_field_mappings[collection_name]
        migrate_collection(collection_name, field_mappings)
    else:
        print(f"Field mappings not found for collection '{collection_name}'. Skipping migration.")

print("Entire MongoDB database migration to DynamoDB completed.")
