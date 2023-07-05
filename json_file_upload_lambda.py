import json
import boto3
import ast 

dynamodb_client = boto3.resource('dynamodb')
def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    response = s3_client.get_object(Bucket = bucket_name, Key = file_key)
    print(f"New file uploaded: s3://{bucket_name}/{file_key}")
    file_reader = response['Body'].read().decode("utf-8")
    file_reader = ast.literal_eval(file_reader)
    file_reader['id'] = str(file_reader['id'])
    table = dynamodb_client.Table('user1')
    table.put_item(Item=file_reader)
    
    return {
        'statusCode': 200,
        'body': 'Lambda function executed successfully'
    }