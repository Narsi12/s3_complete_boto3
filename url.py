import boto3
s3_client = boto3.client('s3')

bucket_name='bucket1202307031547'
object_key='okoklls.json'
response = s3_client.generate_presigned_url('get_object',Params={'Bucket': bucket_name, 'Key': object_key},ExpiresIn=3600)
sliced_response = response[:response.index(object_key)]
Object_URL=sliced_response+object_key
print(Object_URL)




#url LAMBDA FUNCTION

import boto3
import ast

s3_client = boto3.client('s3')
dynamodb_client = boto3.resource('dynamodb')

def lambda_handler(event, context):

    bucket_name='bucket1202307031547'
    
    latest_record = s3_client.list_objects_v2(Bucket=bucket_name)
    object_key = max(latest_record['Contents'], key=lambda obj: obj['LastModified'])['Key']
    print(object_key,"++++++++")
    
    # object_key='allu.json'
    response = s3_client.generate_presigned_url('get_object',Params={'Bucket': bucket_name, 'Key': object_key},ExpiresIn=3600)
    sliced_response = response[:response.index(object_key)]
    Object_URL=sliced_response+object_key
    Object_URL = {"id":object_key,"bucket_name":Object_URL}
    Object_URL['id'] = str(Object_URL['id'])
    table = dynamodb_client.Table('url')
    table.put_item(Item=Object_URL)
    return "Success"