import pymongo
import boto3
import json
from bson import Decimal128
import decimal
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["online_goods_delevery_db"]
mycol = mydb['app_addresssourcedestination']
data = mycol.find()


dynamodb = boto3.resource('dynamodb')

# table = dynamodb.create_table(
#     TableName='delivery_tab',
#     KeySchema=[
#         {
#             'AttributeName': 'ID',
#             'KeyType': 'HASH'
#         }
#     ],
#     AttributeDefinitions=[
#         {
#             'AttributeName': 'ID',
#             'AttributeType': 'S'
#         }
#     ],
#     ProvisionedThroughput={
#         'ReadCapacityUnits': 5,
#         'WriteCapacityUnits': 5
#     }
# )

table = dynamodb.Table('user_info')

def convert_to_dynamodb_format(item):
    dynamodb_item = {
        'ID': str(item['_id']),  # Convert ObjectId to a string for DynamoDB
        'userID': item['userID'],
        'order_type': item['order_type'],
        'qty': item['qty'],
        'temp_order_id': item['temp_order_id'],
        'date_info': item['date_info'].isoformat(),  # Convert datetime to string
        # 'destination_info': item['destination_info'],
        'order_id': item['order_id'],
        # 'source_info': item['source_info'],
        'status': item['status']
    }
    # for key, value in dynamodb_item.items():
    #     if isinstance(value, float):
    #         dynamodb_item[key] = decimal(value)

    return dynamodb_item

# Iterate over the data, transform, and insert into DynamoDB
for item in data:
    dynamodb_item = convert_to_dynamodb_format(item)

    # Insert item into DynamoDB
    table.put_item(Item=dynamodb_item)

print("Data migration to DynamoDB completed.")


  