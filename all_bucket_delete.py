import boto3

from config import aws_access_key_id,aws_secret_access_key

def delete_particular_bucket():
    s3_client = boto3.client('s3')
    response = s3_client.list_buckets()
    buckets = response.get('Buckets', [])
    if buckets:
        for bucket in buckets:
            bucket_name = bucket['Name']
            try:
                s3_client.delete_bucket(Bucket=bucket_name)
                print("Deleted Bucket:", bucket_name, "successfully")
            except Exception as e:
                print(f"Failed to delete bucket {bucket_name}. Error: {str(e)}")
    else:
        print("No buckets found in the S3 service.")

delete_particular_bucket()