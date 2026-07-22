import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.credit_crud import CreditCrudDb
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request import CreditRequest


@pytest.mark.api
class TestCreditRequests:
    def test_credit_requests_valid(
        self,
        api_manager: ApiManager,
        credit_user_request: CreateUserRequest,
        db_session: Session,
    ):
        create_account_response = api_manager.user_steps.create_account(credit_user_request)
        credit_request = RandomModelGenerator.generate(CreditRequest).model_copy(
            update={"accountId": create_account_response.id}
        )

        response = api_manager.user_steps.request_credit(credit_user_request, credit_request)

        assert response.amount == credit_request.amount
        assert response.termMonths == credit_request.termMonths
        assert response.id == create_account_response.id

        credit_from_db = CreditCrudDb.get_credit_by_account_id(db_session, create_account_response.id)

        assert credit_from_db is not None, "кредит не найден в базе"
        assert credit_from_db.id == response.creditId
        assert credit_from_db.account_id == create_account_response.id
        assert credit_from_db.amount == credit_request.amount
        assert credit_from_db.term_months == credit_request.termMonths
        assert credit_from_db.balance == -credit_request.amount

    @pytest.mark.parametrize(
        "amount",
        [pytest.param(4999, id="minimum"), pytest.param(15001, id="maximum")],
    )
    def test_credit_requests_invalid(
        self,
        amount: int,
        api_manager: ApiManager,
        credit_user_request: CreateUserRequest,
        db_session: Session,
    ):
        create_account_response = api_manager.user_steps.create_account(credit_user_request)
        credit_request = RandomModelGenerator.generate(CreditRequest).model_copy(
            update={
                "accountId": create_account_response.id,
                "amount": amount,
            }
        )

        api_manager.user_steps.request_credit_invalid(credit_user_request, credit_request)

        credit_from_db = CreditCrudDb.get_credit_by_account_id(db_session, create_account_response.id)

        assert credit_from_db is None, (
            "Кредит появился в базе после запроса с невалидной суммой"
        )
