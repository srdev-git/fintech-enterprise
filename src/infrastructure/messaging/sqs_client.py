
import os
import boto3
import json

sqs = boto3.client(
    "sqs",
    endpoint_url=os.getenv("AWS_ENDPOINT_URL"),
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test",
)

QUEUE_URL = os.getenv("SQS_QUEUE_URL")

def publish_message(payload: dict):
    sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(payload)
    )
