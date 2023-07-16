 # existing_buckets = s3_client.list_buckets()['Buckets']  2
    # print(existing_buckets)
server="172.16.10.45"

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


# import pyodbc

# mssql_conn = pyodbc.connect(
#     Trusted_Connection='Yes',
#     driver='{SQL Server}',
#     server="172.16.10.45",
#     database="MT_TRAINING"
# )

# mssql_cursor = mssql_conn.cursor()

# tables = mssql_cursor.tables(tableType='TABLE')
# for table in tables:
#     print(table.table_name)









import pyodbc
import mysql.connector

# Connect to MariaDB
maria_conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='students'
)

# Connect to MSSQL
mssql_conn = pyodbc.connect(
    Trusted_Connection='Yes',
    driver='{SQL Server}',
    server="172.16.10.45",
    database="MT_TRAINING"
)

maria_cursor = maria_conn.cursor()

maria_cursor.execute("SHOW TABLES FROM students")
tables = maria_cursor.fetchall()

for table in tables:
    table_name = table[0]
    try:
        maria_cursor.execute(f"SELECT * FROM students.{table_name}")
        rows = maria_cursor.fetchall()
        mssql_cursor = mssql_conn.cursor()

        if not mssql_cursor.tables(table=table_name).fetchone():
            maria_cursor.execute(f"SHOW COLUMNS FROM students.{table_name}")
            columns = maria_cursor.fetchall()
            column_names = [column[0] for column in columns]
            column_types = [column[1].replace('bigint', 'BIGINT') for column in columns]

            create_table_query = f"CREATE TABLE {table_name} ({','.join([f'{name} {type}' for name, type in zip(column_names, column_types)])})"
            mssql_cursor.execute(create_table_query)
        else:
            print(f"Table '{table_name}' already exists in the MSSQL database. Skipping table creation.")

        if mssql_cursor.tables(table=table_name).fetchone():
            pass
            for row in rows:
                bytes_row = [bytes(column, "utf-8") for column in row]
                insert_query = f"INSERT INTO {table_name} VALUES ({','.join(['?'] * len(row))})"
                mssql_cursor.execute(insert_query, bytes_row)
        else:
            print(f"Table '{table_name}' does not exist in the MSSQL database. Skipping insertion.")

        mssql_conn.commit()

    except Exception as e:
        print(f"Error occurred while migrating table '{table_name}': {str(e)}")

mssql_cursor.close()
maria_cursor.close()
maria_conn.close()
mssql_conn.close()

print("Data Migration is completed")



# for table in tables:
#     table_name = table[0]
#     maria_cursor.execute(f"SELECT * FROM {table_name}")
#     table_data = maria_cursor.fetchall()
#     print(f"Data in table '{table_name}':")
#     for row in table_data:
#         print(row)
#     print()