import boto3

s3 = boto3.client('s3')

bucket_name = "aws-code-transcribe"
file_name = input("Enter the local Mp4 file path = ")  # Local file
s3_key = "uploads/greencode.mp4"  # File path in S3

s3.upload_file(file_name, bucket_name, s3_key)
print(f"File uploaded to s3://{bucket_name}/{s3_key}")