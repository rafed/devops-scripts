import boto3

s3 = boto3.resource(
    's3',
    region_name='eu-west-1',
    aws_access_key_id='',
    aws_secret_access_key=''
)
content="String content to write to a new S3 file"

s3.Object('oslofjord', 'test.txt').put(Body=content)
s3.Object('oslofjord', 'test.txt').delete()

