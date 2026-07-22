import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.account_deposit_request import AccountDepositRequest
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestAccountDeposit:
    def test_account_deposit_valid(
        self,
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
        db_session: Session,
    ):
        create_account_response = api_manager.user_steps.create_account(create_user_request)
        account_deposit_request = RandomModelGenerator.generate(AccountDepositRequest).model_copy(
            update={"accountId": create_account_response.id}
        )

        response = api_manager.user_steps.deposit_account(create_user_request, account_deposit_request)

        assert response.balance == account_deposit_request.amount

        account_from_db = AccountCrudDb.get_account_by_id(db_session, create_account_response.id)

        assert account_from_db is not None, "Счет не найден в базе"
        assert account_from_db.balance == account_deposit_request.amount

    @pytest.mark.parametrize(
        "amount",
        [pytest.param(999, id="minimum"), pytest.param(9001, id="maximum")],
    )
    def test_account_deposit_invalid(
        self,
        amount: int,
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
        db_session: Session,
    ):
        create_account_response = api_manager.user_steps.create_account(create_user_request)
        account_deposit_request = AccountDepositRequest(accountId=create_account_response.id, amount=amount)

        api_manager.user_steps.deposit_account_invalid(
            create_user_request, account_deposit_request
        )

        account_from_db = AccountCrudDb.get_account_by_id(db_session, create_account_response.id)

        assert account_from_db is not None, "Счет не найден в базе"
        assert account_from_db.balance == 0, (
            "Баланс изменился после невалидного пополнения"
        )
