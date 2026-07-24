import pytest

from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request import CreditRequest


@pytest.fixture
def credit_request(api_manager, credit_user_request):
    create_account_response = api_manager.user_steps.create_account(
        credit_user_request
    )

    request = RandomModelGenerator.generate(CreditRequest).model_copy(
        update={
            "accountId": create_account_response.id
        }
    )

    return request


@pytest.fixture
def invalid_credit_request(request, api_manager, credit_user_request):
    amount = request.param

    create_account_response = api_manager.user_steps.create_account(credit_user_request)
    credit_request = RandomModelGenerator.generate(CreditRequest).model_copy(
        update={
            "accountId": create_account_response.id,
            "amount": amount,
        }
    )

    return credit_request


@pytest.fixture
def credit_repay_request(api_manager, credit_user_request):

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

    return credit_repay_request

@pytest.fixture
def invalid_credit_repay_request(request, api_manager, credit_user_request):

    amount = request.param

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


    return credit_repay_request


