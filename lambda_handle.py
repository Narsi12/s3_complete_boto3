import json
import boto3
import logging
from custom_encoder import CustomEncoder


logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb_table = 'crud'
dynamodb = boto3.client('dynamodb')
table = dynamodb.Table(dynamodb_table)

getMethod = 'GET'
postMethod = 'POST'
pathchMethod = 'PATCH'
deleteMethod = 'DELETE'
employee = '/employee'



def lambda_handler(event, context):
    logger.info(event)
    httpMethod = event['httpMethod']
    path = event['path']
    if httpMethod == getMethod and path == employee:
        response = buildResponse(200)
    elif httpMethod == postMethod and path == employee:
        response = buildResponse(200)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def buildResponse(statusCode, body = None):
    response = {
        'statusCode':statusCode,
        'headers':{
            'Content-Type' : 'application/json',
            'Access-Control-Allow-Origin':'*'
        }
    }
    if body is not None:
        response['body'] = json.dumps(body, cls = CustomEncoder)
    return response