import os
import json
import time
import logging
import boto3
from botocore.exceptions import ClientError
from sqlalchemy.exc import SQLAlchemyError

from src.infrastructure.database.session import SessionLocal
from src.infrastructure.database.init_db import init_db
from src.infrastructure.database.transaction_repository_impl import (
    TransactionRepositoryImpl,
)
from src.application.services.process_transaction import ProcessTransactionService


# ==============================
# CONFIGURAÇÃO
# ==============================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

AWS_ENDPOINT = os.getenv("AWS_ENDPOINT_URL")
QUEUE_NAME = os.getenv("SQS_QUEUE_NAME", "transactions")


# ==============================
# SQS CLIENT
# ==============================

sqs = boto3.client(
    "sqs",
    endpoint_url=AWS_ENDPOINT,
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test",
)


# ==============================
# INFRA BOOTSTRAP
# ==============================

def wait_for_sqs():
    """Aguarda o SQS ficar disponível"""
    logger.info("Aguardando SQS...")
    while True:
        try:
            sqs.list_queues()
            logger.info("SQS disponível.")
            break
        except Exception:
            time.sleep(2)


def ensure_queue_exists():
    """Cria fila automaticamente se não existir"""
    try:
        response = sqs.get_queue_url(QueueName=QUEUE_NAME)
        queue_url = response["QueueUrl"]
        logger.info(f"Fila encontrada: {queue_url}")
        return queue_url
    except ClientError:
        logger.info(f"Criando fila: {QUEUE_NAME}")
        response = sqs.create_queue(
            QueueName=QUEUE_NAME,
            Attributes={
                "VisibilityTimeout": "30",
                "MessageRetentionPeriod": "86400"
            }
        )
        queue_url = response["QueueUrl"]
        logger.info(f"Fila criada: {queue_url}")
        return queue_url


# ==============================
# MESSAGE HANDLER (ORQUESTRADOR)
# ==============================

def handle_message(payload: dict):
    """
    Worker NÃO contém regra de negócio.
    Ele apenas resolve dependências e chama o caso de uso.
    """

    session = SessionLocal()

    try:
        repository = TransactionRepositoryImpl(session)
        service = ProcessTransactionService(repository)

        service.execute(payload)

        logger.info(f"Transação processada: {payload['external_id']}")

    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Erro de banco: {e}")
        raise

    except Exception as e:
        logger.error(f"Erro no processamento: {e}")
        raise

    finally:
        session.close()


# ==============================
# LOOP PRINCIPAL
# ==============================

def main():
    logger.info("Inicializando Worker...")

    init_db()
    wait_for_sqs()
    queue_url = ensure_queue_exists()

    logger.info("Worker iniciado. Aguardando mensagens...")

    while True:
        try:
            response = sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=10
            )

            messages = response.get("Messages", [])

            for message in messages:
                try:
                    body = json.loads(message["Body"])

                    logger.info(f"Mensagem recebida: {body}")

                    handle_message(body)
                    
                    sqs.delete_message(
                        QueueUrl=queue_url,
                        ReceiptHandle=message["ReceiptHandle"]
                    )

                    logger.info("Mensagem removida da fila.")

                except Exception:
                    logger.warning("Falha no processamento. Mensagem não removida.")
                    # SQS fará retry automaticamente após VisibilityTimeout

        except Exception as e:
            logger.error(f"Erro no loop principal: {e}")
            time.sleep(5)


if __name__ == "__main__":
    main()