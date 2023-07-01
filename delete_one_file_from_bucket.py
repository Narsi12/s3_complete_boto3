import boto3

from config import aws_access_key_id,aws_secret_access_key

def delete_particular_file_from_s3_bucket(bucket_name,file_name):
    s3_client = boto3.client('s3',
                             aws_access_key_id=aws_access_key_id,
                             aws_secret_access_key=aws_secret_access_key)
    try:
        s3_client.delete_object(Bucket = bucket_name, Key = file_name)
        print(f"File {file_name} deleted from bucket {bucket_name} successfully!")
    except Exception as e:
        print(f"Failed to delete file {file_name} from bucket {bucket_name}. Error: {str(e)}")

bucket_name = 'yellow202307011256'
file_name = 'screenshot1.jpg'
delete_particular_file_from_s3_bucket(bucket_name, file_name)
