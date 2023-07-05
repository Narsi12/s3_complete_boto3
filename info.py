 # existing_buckets = s3_client.list_buckets()['Buckets']  2
    # print(existing_buckets)


import pymongo
import boto3
from bson import ObjectId
from decimal import Decimal
import botocore
from datetime import datetime

# MongoDB configuration
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["online_goods_delevery_db"]

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
    elif isinstance(data, ObjectId):
        return str(data)
    else:
        return data

def create_dynamodb_table(collection_name):
    table_name = table_name_prefix + collection_name

    try:
        dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'ID',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'ID',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print(f"Table '{table_name}' created successfully!")

    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print(f"Table '{table_name}' already exists.")
        else:
            print("An error occurred:", e)

def migrate_collection(collection_name):
    collection = mongo_db[collection_name]
    dynamodb_table = dynamodb.Table(table_name_prefix + collection_name)

    data = collection.find()
    for item in data:
        item = convert_float_values_to_strings(item)
        dynamodb_item = {}

        if 'ID' in item:
            dynamodb_item['ID'] = str(item['ID'])
        else:
            dynamodb_item['ID'] = 'id-v1'

        for key, value in item.items():
            if key == 'ID':
                continue
            if isinstance(value, Decimal):
                value = float(value)
            elif isinstance(value, datetime):
                value = value.isoformat()
            dynamodb_item[key] = value

        dynamodb_table.put_item(Item=dynamodb_item)

    print(f"Data migration for collection '{collection_name}' completed.")

# Iterate through all collections in the MongoDB database
collection_names = mongo_db.list_collection_names()
for collection_name in collection_names:
    create_dynamodb_table(collection_name)

# Migrate the collections to DynamoDB
for collection_name in collection_names:
    migrate_collection(collection_name)

print("Entire MongoDB database migration to DynamoDB completed.")
