from decimal import Decimal
from src.domain.entities.transaction import Transaction

class ProcessTransactionService:

    def __init__(self, repository):
        self.repository = repository

    def execute(self, payload: dict):

        if self.repository.exists_by_external_id(payload["external_id"]):
            return

        transaction = Transaction(
            external_id=payload["external_id"],
            amount=Decimal(str(payload["amount"]))
        )

        transaction.process()

        self.repository.save(transaction)