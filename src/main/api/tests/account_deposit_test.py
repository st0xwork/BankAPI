import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.models.account_deposit_request import AccountDepositRequest
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestAccountDeposit:
    def test_account_deposit_valid(
        self,
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
        account_deposit_request: AccountDepositRequest,
        db_session: Session,
    ):
        response = api_manager.user_steps.deposit_account(create_user_request, account_deposit_request)

        assert response.balance == account_deposit_request.amount, (
            "Баланс аккаунта должен быть равен сумме депозита"
        )

        account_from_db = AccountCrudDb.get_account_by_id(db_session, response.id)

        assert account_from_db.balance == account_deposit_request.amount, (
            "Баланс аккаунта в БД должен быть равен сумме депозита"
        )

    @pytest.mark.parametrize(
        "invalid_account_deposit_request",
        [pytest.param(999, id="minimum"), pytest.param(9001, id="maximum")],
        indirect=True
    )
    def test_account_deposit_invalid(
        self,
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
        invalid_account_deposit_request: AccountDepositRequest,
        db_session: Session,
    ):

        api_manager.user_steps.deposit_account_invalid(create_user_request, invalid_account_deposit_request)


        account_from_db = AccountCrudDb.get_account_by_id(db_session, invalid_account_deposit_request.accountId)

        assert account_from_db.balance == 0, (
            "Баланс в БД изменился после невалидного пополнения"
        )
