import time
import boto3
import requests

from S3bucket_store import bucket_name, s3_key

transcribe = boto3.client('transcribe')

job_name = "aws-transcription-greencode-job"
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
    if status["TranscriptionJob"]["TranscriptionJobStatus"] in ["COMPLETED", "FAILED"]:
        break
    time.sleep(5)

# Check if transcription was successful
if status["TranscriptionJob"]["TranscriptionJobStatus"] == "COMPLETED":
    # Get the URL of the transcript file
    transcript_url = status["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
    print(f"Downloading transcription from: {transcript_url}")

    # Download the transcript file
    response = requests.get(transcript_url)
    transcript_data = response.json()

    # Extract text from transcript JSON
    transcript_text = transcript_data["results"]["transcripts"][0]["transcript"]

    # Save to a text file
    transcript_location = input("Enter the location to save the transcribe file = ")
    with open(transcript_location, "w", encoding="utf-8") as f:
        f.write(transcript_text)

    print("Transcription saved to transcription.txt")
else:
    print("Transcription failed.")