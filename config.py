import uuid
import datetime
aws_access_key_id = "AKIARY57NE7BDRTSPZSJ"
aws_secret_access_key = "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"
region = "us-east-1"

def create_bucket_name(bucket_prefix):
    current_datetime = datetime.datetime.now().strftime('%Y%m%d%H%S')
    order_number = current_datetime 
    return ''.join([bucket_prefix,current_datetime])