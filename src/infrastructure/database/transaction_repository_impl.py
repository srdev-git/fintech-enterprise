from src.domain.repositories.transaction_repository import TransactionRepository
from src.infrastructure.database.models import Transaction as TransactionModel
from src.domain.entities.transaction import Transaction

class TransactionRepositoryImpl(TransactionRepository):

    def __init__(self, session):
        self.session = session

    def exists_by_external_id(self, external_id: str) -> bool:
        return (
            self.session.query(TransactionModel)
            .filter_by(external_id=external_id)
            .first()
            is not None
        )

    def save(self, transaction: Transaction):
        model = TransactionModel(
            external_id=transaction.external_id,
            amount=transaction.amount,
            status=transaction.status
        )
        self.session.add(model)
        self.session.commit()