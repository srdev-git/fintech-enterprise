from fastapi import APIRouter
import boto3
import os
import json
from src.infrastructure.database.init_db import init_db
router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.on_event("startup")
def startup():
    init_db()

@router.post("/publish")
def publish(payload: dict):
    sqs = boto3.client(
        "sqs",
        endpoint_url=os.getenv("AWS_ENDPOINT_URL"),
        region_name="us-east-1",
        aws_access_key_id="test",
        aws_secret_access_key="test",
    )

    queue_name = os.getenv("SQS_QUEUE_NAME", "transactions")

    response = sqs.get_queue_url(QueueName=queue_name)
    queue_url = response["QueueUrl"]

    sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(payload)
    )

    return {"message": "Mensagem enviada para fila"}