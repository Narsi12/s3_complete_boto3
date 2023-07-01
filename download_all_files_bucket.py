import boto3
from config import aws_access_key_id,aws_secret_access_key


def download_all_files_from_bucket(bucket_name, local_directory):
    s3_client = boto3.client('s3',
                             aws_access_key_id=aws_access_key_id,
                             aws_secret_access_key=aws_secret_access_key
                             )
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            for obj in response['Contents']:
                key = obj['Key']
                local_path = f"{local_directory}/{key}"
                print(local_path)
                s3_client.download_file(bucket_name, key, local_path)
                print(f"File {key} downloaded to {local_path} successfully!")
        else:
            print("No files found in the bucket.")
    except Exception as e:
        print(f"Failed to download files from bucket {bucket_name}. Error: {str(e)}")

bucket_name = 'yellow202307011256'
local_directory = 'C:/Users/narsimhac/Pictures/Camera Roll'

download_all_files_from_bucket(bucket_name, local_directory)

 