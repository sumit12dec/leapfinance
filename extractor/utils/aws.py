import os

import boto3
from botocore.exceptions import ClientError

ACCESS_KEY_ID = os.environ.get('ACCESS_KEY_ID', None)
SECRET_ACCESS_KEY = os.environ.get('SECRET_ACCESS_KEY', None)

def get_boto_session():
	session = boto3.Session(
    	aws_access_key_id=ACCESS_KEY_ID,
    	aws_secret_access_key=SECRET_ACCESS_KEY,
	)

	return session


def upload_to_s3(contents, file_name, bucket):
    """Upload a file to an S3 bucket"""


    s3_client = boto3.client('s3',
    		aws_access_key_id = ACCESS_KEY_ID,
    		aws_secret_access_key = SECRET_ACCESS_KEY)
	
    id = None

    # Write id to S3
    s3_client.put_object(Body=contents, Bucket=bucket, Key=file_name)

    # Read id from S3
    # data = s3.get_object(Bucket=bucket, Key=key)
    # id = data.get('Body').read().decode('utf-8') 
    # logger.info("Id:" + id)


