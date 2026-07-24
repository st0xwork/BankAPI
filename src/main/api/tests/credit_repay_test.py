import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.db.crud.credit_crud import CreditCrudDb
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest


@pytest.mark.api
class TestCreditRepay:
    def test_credit_repay_valid(
        self,
        api_manager: ApiManager,
        credit_user_request: CreateUserRequest,
        credit_repay_request: CreditRepayRequest,
        db_session: Session,
    ):

        response = api_manager.user_steps.repay_credit(credit_user_request, credit_repay_request)

        assert response.creditId == credit_repay_request.creditId, (
            "В ответе указан неверный ID погашенного кредита"
        )

        assert response.amountDeposited == credit_repay_request.amount, (
            "Сумма погашения в ответе не совпадает с отправленной суммой"
        )

        credit_from_db = CreditCrudDb.get_credit_by_account_id(db_session, credit_repay_request.accountId)
        account_from_db = AccountCrudDb.get_account_by_id(db_session, credit_repay_request.accountId)


        assert credit_from_db.balance == 0, (
            "Задолженность по кредиту в БД не была погашена"
        )
        assert account_from_db.balance == 0, (
            "После погашения кредита деньги не были списаны со счета"
        )

    @pytest.mark.parametrize(
        "invalid_credit_repay_request",
        [pytest.param(-1, id="underpayment"), pytest.param(1, id="overpayment")],
        indirect=True
    )
    def test_credit_repay_invalid(
        self,
        api_manager: ApiManager,
        credit_user_request: CreateUserRequest,
        invalid_credit_repay_request: CreditRepayRequest,
        db_session: Session,
    ):


        api_manager.user_steps.repay_credit_invalid(credit_user_request, invalid_credit_repay_request)

        credit_from_db = CreditCrudDb.get_credit_by_account_id(db_session, invalid_credit_repay_request.accountId)
        account_from_db = AccountCrudDb.get_account_by_id(db_session, invalid_credit_repay_request.accountId)

        assert credit_from_db.balance == -credit_from_db.amount, (
            "Долг изменился после невалидного погашения"
        )
        assert account_from_db.balance == credit_from_db.amount, (
            "Баланс счета изменился после невалидного погашения"
        )
