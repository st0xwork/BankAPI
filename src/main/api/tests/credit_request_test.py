import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.credit_crud import CreditCrudDb
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request import CreditRequest


@pytest.mark.api
class TestCreditRequests:
    def test_credit_requests_valid(
        self,
        api_manager: ApiManager,
        credit_user_request: CreateUserRequest,
        credit_request: CreditRequest,
        db_session: Session,
    ):


        response = api_manager.user_steps.request_credit(credit_user_request, credit_request)

        assert response.amount == credit_request.amount, (
            "Сумма выданного кредита не совпадает с запрошенной суммой"
        )

        credit_from_db = CreditCrudDb.get_credit_by_account_id(db_session, credit_request.accountId)

        assert credit_from_db.account_id == credit_request.accountId, (
            "Кредит в БД привязан к неправильному счет"
        )

        assert credit_from_db.balance == -credit_request.amount, (
            "Задолженность в БД не соответствует сумме выданного кредита"
        )


    @pytest.mark.parametrize(
        "invalid_credit_request",
        [pytest.param(4999, id="minimum"), pytest.param(15001, id="maximum")],
        indirect=True
    )
    def test_credit_requests_invalid(
        self,
        api_manager: ApiManager,
        credit_user_request: CreateUserRequest,
        invalid_credit_request: CreditRequest,
        db_session: Session,
    ):

        api_manager.user_steps.request_credit_invalid(credit_user_request, invalid_credit_request)

        credit_exists = CreditCrudDb.credit_exists(db_session, invalid_credit_request.accountId)

        assert not credit_exists, (
            "Кредит появился в БД после запроса с невалидной суммой"
        )



