import json
import boto3


def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    print(bucket_name,"+_+__+_+_")
    print(file_key,"???????")
    response = s3_client.get_object(Bucket = bucket_name, Key = file_key)
    print(response)
    print(f"New file uploaded: s3://{bucket_name}/{file_key}")
    
    return {
        'statusCode': 200,
        'body': 'Lambda function executed successfully'
    }
