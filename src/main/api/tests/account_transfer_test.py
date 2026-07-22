import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.account_deposit_request import AccountDepositRequest
from src.main.api.models.account_transfer_request import AccountTransferRequest
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestAccountTransfer:
    def test_account_transfer_valid(
        self,
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
        db_session: Session,
    ):
        from_account_response = api_manager.user_steps.create_account(create_user_request)
        to_account_response = api_manager.user_steps.create_account(create_user_request)

        account_deposit_request = RandomModelGenerator.generate(AccountDepositRequest).model_copy(
            update={"accountId": from_account_response.id}
        )
        api_manager.user_steps.deposit_account(create_user_request, account_deposit_request)

        account_transfer_request = RandomModelGenerator.generate(
            AccountTransferRequest
        ).model_copy(
            update={
                "fromAccountId": from_account_response.id,
                "toAccountId": to_account_response.id,
                "amount": account_deposit_request.amount,
            }
        )
        response = api_manager.user_steps.transfer_account(create_user_request, account_transfer_request)

        assert response.fromAccountIdBalance == 0

        from_account_db = AccountCrudDb.get_account_by_id(db_session, from_account_response.id)
        to_account_db = AccountCrudDb.get_account_by_id(db_session, to_account_response.id)

        assert from_account_db is not None
        assert to_account_db is not None
        assert from_account_db.balance == 0
        assert to_account_db.balance == account_transfer_request.amount

    @pytest.mark.parametrize(
        "amount",
        [pytest.param(499, id="minimum"), pytest.param(10001, id="maximum")],
    )
    def test_account_transfer_invalid(
        self,
        amount: int,
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
        db_session: Session,
    ):
        from_account_response = api_manager.user_steps.create_account(create_user_request)
        to_account_response = api_manager.user_steps.create_account(create_user_request)

        balance = 0
        while balance < amount:
            account_deposit_request = RandomModelGenerator.generate(AccountDepositRequest).model_copy(
                update={"accountId": from_account_response.id}
            )
            deposit_response = api_manager.user_steps.deposit_account(
                create_user_request, account_deposit_request
            )
            balance = deposit_response.balance

        account_transfer_request = AccountTransferRequest(
            fromAccountId=from_account_response.id,
            toAccountId=to_account_response.id,
            amount=amount,
        )

        response = api_manager.user_steps.transfer_account_invalid(
            create_user_request, account_transfer_request
        )

        assert response.status_code == 400

        from_account_db = AccountCrudDb.get_account_by_id(db_session, from_account_response.id)
        to_account_db = AccountCrudDb.get_account_by_id(db_session, to_account_response.id)

        assert from_account_db is not None
        assert to_account_db is not None

        assert from_account_db.balance == balance, (
            "Баланс отправителя изменился после невалидного перевода"
        )
        assert to_account_db.balance == 0, (
            "На счёт получателя поступили деньги после невалидного перевода"
        )
