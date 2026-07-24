import pytest

from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.account_deposit_request import AccountDepositRequest
from src.main.api.models.account_transfer_request import AccountTransferRequest



@pytest.fixture
def account_deposit_request(api_manager, create_user_request):
    create_account_response = api_manager.user_steps.create_account(create_user_request)

    deposit_request = RandomModelGenerator.generate(AccountDepositRequest).model_copy(
        update={"accountId": create_account_response.id}
    )

    return deposit_request

@pytest.fixture
def invalid_account_deposit_request(request, api_manager, create_user_request):
    amount = request.param

    create_account_response = api_manager.user_steps.create_account(create_user_request)

    deposit_request = AccountDepositRequest(
        accountId=create_account_response.id,
        amount=amount
    )

    return deposit_request



@pytest.fixture
def account_transfer_request(api_manager, create_user_request):
    from_account_response = api_manager.user_steps.create_account(create_user_request)
    to_account_response = api_manager.user_steps.create_account(create_user_request)

    account_deposit_request = RandomModelGenerator.generate(AccountDepositRequest).model_copy(
        update={
            "accountId": from_account_response.id
        }
    )
    api_manager.user_steps.deposit_account(create_user_request, account_deposit_request)

    account_transfer_request = RandomModelGenerator.generate(AccountTransferRequest).model_copy(
        update={
            "fromAccountId": from_account_response.id,
            "toAccountId": to_account_response.id,
            "amount": account_deposit_request.amount,
        }
    )

    return account_transfer_request

@pytest.fixture
def invalid_account_transfer_request(request, api_manager, create_user_request):
    amount = request.param

    from_account_response = api_manager.user_steps.create_account(create_user_request)
    to_account_response = api_manager.user_steps.create_account(create_user_request)

    account_deposit_request = AccountDepositRequest(
        accountId=from_account_response.id,
        amount=9000,
    )

    api_manager.user_steps.deposit_account(create_user_request, account_deposit_request)
    api_manager.user_steps.deposit_account(create_user_request, account_deposit_request)

    account_transfer_request = AccountTransferRequest(
        fromAccountId=from_account_response.id,
        toAccountId=to_account_response.id,
        amount=amount,
    )

    return account_transfer_request

