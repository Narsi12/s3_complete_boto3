import uuid
import datetime
aws_access_key_id = "<Your access key>"
aws_secret_access_key = "<Your screat key>"
region = "us-east-1"

def create_bucket_name(bucket_prefix):
    current_datetime = datetime.datetime.now().strftime('%Y%m%d%H%S')
    order_number = current_datetime 
    return ''.join([bucket_prefix,current_datetime])
