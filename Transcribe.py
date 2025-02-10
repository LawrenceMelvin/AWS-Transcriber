import time
import boto3

from S3bucket_store import bucket_name, s3_key

transcribe = boto3.client('transcribe')

job_name = "aws-transcription-job"
s3_uri = f"s3://{bucket_name}/{s3_key}"

response = transcribe.start_transcription_job(
    TranscriptionJobName=job_name,
    Media={'MediaFileUri': s3_uri},
    MediaFormat='mp4',  # Change format if needed
    LanguageCode='en-US'
)

print("Transcription started. Waiting for completion...")

# Wait for the job to complete
while True:
    status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
        break
    time.sleep(5)

if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
    transcript_url = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
    print(f"Transcription completed. Download result: {transcript_url}")
else:
    print("Transcription failed.")