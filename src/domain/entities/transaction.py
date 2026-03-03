from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Transaction:
    external_id: str
    amount: Decimal
    status: str = "PENDING"

    def process(self):
        self.status = "PROCESSED"