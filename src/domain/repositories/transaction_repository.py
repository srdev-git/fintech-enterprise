from abc import ABC, abstractmethod
from src.domain.entities.transaction import Transaction

class TransactionRepository(ABC):

    @abstractmethod
    def save(self, transaction: Transaction):
        pass

    @abstractmethod
    def exists_by_external_id(self, external_id: str) -> bool:
        pass