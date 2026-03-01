# app/utils/s3_uploader.py

import boto3
import os
from botocore.client import Config

class S3Uploader:
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            endpoint_url=os.getenv("AWS_S3_ENDPOINT"),
            region_name=os.getenv("AWS_S3_REGION"),
            config=Config(signature_version="s3v4")
        )
        self.bucket = os.getenv("AWS_S3_BUCKET")

    def upload_file(self, file_obj, filename: str):
        self.s3.upload_fileobj(file_obj, self.bucket, filename)
        return f"{self.bucket}/{filename}"