import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.models.account_transfer_request import AccountTransferRequest
from src.main.api.models.create_user_request import CreateUserRequest

@pytest.mark.api
class TestAccountTransfer:
    def test_account_transfer_valid(
        self,
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
        account_transfer_request: AccountTransferRequest,
        db_session: Session,
    ):

        response = api_manager.user_steps.transfer_account(create_user_request, account_transfer_request)

        assert response.fromAccountIdBalance == 0, (
            "После перевода баланс исходного счета должен быть равен 0"
        )

        from_account_db = AccountCrudDb.get_account_by_id(db_session, account_transfer_request.fromAccountId)
        to_account_db = AccountCrudDb.get_account_by_id(db_session, account_transfer_request.toAccountId)

        assert from_account_db.balance == 0, (
            "Баланс исходного счета в БД должен быть равен 0"
        )
        assert to_account_db.balance == account_transfer_request.amount, (
            "Баланс счета получателя в БД должен быть равен сумме перевода"
        )

    @pytest.mark.parametrize(
        "invalid_account_transfer_request",
        [
            pytest.param(499, id="minimum"),
            pytest.param(10001, id="maximum"),
        ],
        indirect=True,
    )
    def test_account_transfer_invalid(
            self,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest,
            invalid_account_transfer_request: AccountTransferRequest,
            db_session: Session,
    ):
        api_manager.user_steps.transfer_account_invalid(
            create_user_request,
            invalid_account_transfer_request,
        )

        from_account_db = AccountCrudDb.get_account_by_id(
            db_session,
            invalid_account_transfer_request.fromAccountId,
        )
        to_account_db = AccountCrudDb.get_account_by_id(
            db_session,
            invalid_account_transfer_request.toAccountId,
        )

        assert from_account_db.balance == 18000, (
            "Баланс отправителя изменился в БД после невалидного перевода"
        )
        assert to_account_db.balance == 0, (
            "На счёт получателя в БД поступили деньги после невалидного перевода"
        )
