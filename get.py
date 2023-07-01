import boto3

from config import aws_access_key_id,aws_secret_access_key

def get():
    s3_client = boto3.client('s3',
                             aws_access_key_id=aws_access_key_id,
                             aws_secret_access_key=aws_secret_access_key
                             )
    try:
        response = s3_client.list_buckets()['Buckets']
        buckets = [bucket['Name'] for bucket in response]
        print({'buckets':buckets})
    except Exception as e:
        print({"message": f"Failed to retrieve bucket names. Error: {str(e)}"})

get()