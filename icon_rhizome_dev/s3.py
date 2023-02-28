import boto3

from icon_rhizome_dev import ENV


class S3:
    def __init__(self) -> None:
        self.bucket = "tools-rhizome-dev"
        self.aws_access_key = ENV["AWS_ACCESS_KEY"]
        self.aws_secret_key = ENV["AWS_SECRET_KEY"]
        self.client = boto3.client(
            service_name="s3",
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key,
        )

    def upload_file(self, filename, data):
        response = self.client.put_object(
            Body=data,
            Bucket=self.bucket,
            Key=filename,
        )
        return response
