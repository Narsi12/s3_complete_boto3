import boto3

from config import aws_access_key_id,aws_secret_access_key

def delete_all_files_from_s3_bucket(bucket_name):
    s3_client = boto3.client('s3',
                             aws_access_key_id=aws_access_key_id,
                             aws_secret_access_key=aws_secret_access_key)
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            objects = []
            for obj in response['Contents']:
                objects.append({'Key':obj['Key']})
            response=s3_client.delete_objects(
                Bucket = bucket_name,
                Delete = {'Objects':objects}
            )
            print(response)
            deleted_objects = response.get('Deleted', [])
            print(f"{len(deleted_objects)} files deleted from the bucket.")
        else:
            print("No files found in the bucket.")
    except Exception as e:
         print(f"Failed to delete files from bucket {bucket_name}. Error: {str(e)}")

bucket_name = 'yellow202307011256'
delete_all_files_from_s3_bucket(bucket_name)