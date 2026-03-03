import pytest
from unittest.mock import Mock
from decimal import Decimal

from src.application.services.process_transaction import ProcessTransactionService


def test_deve_salvar_transacao_quando_nao_existe():

    # Arrange
    repository_mock = Mock()
    repository_mock.exists_by_external_id.return_value = False

    service = ProcessTransactionService(repository_mock)

    payload = {
        "external_id": "abc123",
        "amount": 100
    }

    # Act
    service.execute(payload)

    # Assert
    repository_mock.save.assert_called_once()


def test_nao_deve_salvar_se_ja_existir():

    # Arrange
    repository_mock = Mock()
    repository_mock.exists_by_external_id.return_value = True

    service = ProcessTransactionService(repository_mock)

    payload = {
        "external_id": "abc123",
        "amount": 100
    }

    # Act
    service.execute(payload)

    # Assert
    repository_mock.save.assert_not_called()