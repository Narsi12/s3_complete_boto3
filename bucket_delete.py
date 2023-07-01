import boto3

from config import aws_access_key_id,aws_secret_access_key

def delete_particular_bucket(bucket_name):
    s3_client = boto3.client('s3')
    try:
        s3_client.delete_bucket(Bucket = bucket_name)
        print("Deleted Bucket: ",bucket_name," successfully")
    except Exception as e:
        print(f"Failed to delete bucket {bucket_name}. Error: {str(e)}")

bucket_name='yellow202307011256'
delete_particular_bucket(bucket_name)
    