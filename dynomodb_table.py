import boto3
import botocore

dynamodb = boto3.resource('dynamodb')

try:
    table = dynamodb.create_table(
        TableName='delivery',
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
    print("Table created successfully!")

except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == 'ResourceInUseException':
        print("Table already exists.")
    else:
        print("An error occurred:", e)