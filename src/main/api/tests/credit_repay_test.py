import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.db.crud.credit_crud import CreditCrudDb
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request import CreditRequest


@pytest.mark.api
class TestCreditRepay:
    def test_credit_repay_valid(
        self,
        api_manager: ApiManager,
        credit_user_request: CreateUserRequest,
        db_session: Session,
    ):
        create_account_response = api_manager.user_steps.create_account(credit_user_request)
        credit_request = RandomModelGenerator.generate(CreditRequest).model_copy(
            update={"accountId": create_account_response.id}
        )
        credit_response = api_manager.user_steps.request_credit(credit_user_request, credit_request)

        credit_repay_request = RandomModelGenerator.generate(CreditRepayRequest).model_copy(
            update={
                "creditId": credit_response.creditId,
                "accountId": create_account_response.id,
                "amount": credit_response.amount,
            }
        )
        response = api_manager.user_steps.repay_credit(credit_user_request, credit_repay_request)

        assert response.creditId == credit_response.creditId
        assert response.amountDeposited == credit_response.amount

        credit_from_db = CreditCrudDb.get_credit_by_account_id(db_session, create_account_response.id)
        account_from_db = AccountCrudDb.get_account_by_id(db_session, create_account_response.id)

        assert credit_from_db is not None, "Кредит не найден в базе"
        assert account_from_db is not None, "Счет не найден в базе"

        assert credit_from_db.balance == 0, "Кредит нее был полностью погашен"
        assert account_from_db.balance == 0, "Деньги не были списаны со счета"

    @pytest.mark.parametrize(
        "amount",
        [pytest.param(-1, id="underpayment"), pytest.param(1, id="overpayment")],
    )
    def test_credit_repay_invalid(
        self,
        amount: int,
        api_manager: ApiManager,
        credit_user_request: CreateUserRequest,
        db_session: Session,
    ):
        create_account_response = api_manager.user_steps.create_account(credit_user_request)
        credit_request = RandomModelGenerator.generate(CreditRequest).model_copy(
            update={"accountId": create_account_response.id}
        )
        credit_response = api_manager.user_steps.request_credit(credit_user_request, credit_request)

        credit_repay_request = RandomModelGenerator.generate(CreditRepayRequest).model_copy(
            update={
                "creditId": credit_response.creditId,
                "accountId": create_account_response.id,
                "amount": credit_response.amount + amount,
            }
        )

        api_manager.user_steps.repay_credit_invalid(credit_user_request, credit_repay_request)

        credit_from_db = CreditCrudDb.get_credit_by_account_id(db_session, create_account_response.id)
        account_from_db = AccountCrudDb.get_account_by_id(db_session, create_account_response.id)

        assert credit_from_db is not None, "Кредит найден в базе"
        assert account_from_db is not None, "Счет найден в базе"

        assert credit_from_db.balance == -credit_response.amount, (
            "Долг изменился после невалидного погашения"
        )
        assert account_from_db.balance == credit_response.amount, (
            "Баланс счета изменился после невалидного погашения"
        )
