import boto3

s3 = boto3.client('s3')

bucket_name = "aws-code-transcribe"
file_name = "C:\\Users\\Lawrence Melvin\\Downloads\\TEDx.mp4"  # Local file
s3_key = "uploads/TEDx.mp4"  # File path in S3

s3.upload_file(file_name, bucket_name, s3_key)
print(f"File uploaded to s3://{bucket_name}/{s3_key}")