import boto3
import os
from config import aws_access_key_id,aws_secret_access_key

def download_file_from_s3_bucket(bucket_name,file_name,local_path):
    s3_client = boto3.client('s3',
                             aws_access_key_id=aws_access_key_id,
                             aws_secret_access_key=aws_secret_access_key
                             )
    try:
        local_file_path = os.path.join(local_path, file_name)
        s3_client.download_file(bucket_name,file_name,local_file_path)
        print(f"File {file_name} downloaded to {local_path} successfully!")
    except Exception as e:
        print(f"Failed to download file {file_name} from bucket {bucket_name}. Error: {str(e)}")
        return False

download_file_from_s3_bucket('chirusimha','screenshot1.jpg', 'C:/Users/narsimhac/Pictures/Camera Roll')
