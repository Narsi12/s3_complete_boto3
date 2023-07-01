import boto3

from config import aws_access_key_id,aws_secret_access_key

def upload_file(bucket_name,file_path,key,file_type):
    file_extension = f".{file_type}"
    key_with_extension = f"{key}{file_extension}"

    s3_client = boto3.client('s3',
                             aws_access_key_id=aws_access_key_id,
                             aws_secret_access_key=aws_secret_access_key
                             )
    try:
        s3_client.upload_file(file_path, bucket_name, key_with_extension)
        print({"message": f"File {file_path} uploaded to bucket {bucket_name} successfully!"})
        return True
    except Exception as e:
        print({"message": f"Failed to upload file to bucket. Error: {str(e)}"})
        return False

upload_file('yellow202307011256',"C:/Users/narsimhac/Pictures/Camera Roll/WIN_20221121_16_51_02_Pro.jpg",'photo','jpg')
# upload_file('chirusimha',"C:/Users/narsimhac/Pictures/Screenshots/Screenshot (100).png",'screenshot','jpg')