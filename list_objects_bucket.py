import boto3

from config import aws_access_key_id,aws_secret_access_key

def list_objects_in_particular_bucket(bucket_name):
    s3_client = boto3.client('s3',
                             aws_access_key_id=aws_access_key_id,
                             aws_secret_access_key=aws_secret_access_key
                             )
    try:
        response = s3_client.list_objects_v2(Bucket = bucket_name)['Contents']
        keys = [obj['Key'] for obj in response]
        print({"message": f"Number of files in bucket {bucket_name}: {keys}"})
    except Exception as e:
        print({"message": f"Failed to count files in bucket. Error: {str(e)}"})
        return None

list_objects_in_particular_bucket('yellow202307011400')