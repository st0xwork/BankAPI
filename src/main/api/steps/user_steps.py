from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.account_deposit_request import AccountDepositRequest
from src.main.api.models.account_transfer_request import AccountTransferRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_created(),
        ).post(None)
        return response

    def deposit_account(
        self,
        create_user_request: CreateUserRequest,
        account_deposit_request: AccountDepositRequest,
    ):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.ACCOUNT_DEPOSIT,
            ResponseSpecs.request_ok(),
        ).post(account_deposit_request)
        return response

    def deposit_account_invalid(
        self,
        create_user_request: CreateUserRequest,
        account_deposit_request: AccountDepositRequest,
    ):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.ACCOUNT_DEPOSIT,
            ResponseSpecs.request_bad(),
        ).post(account_deposit_request)
        return response

    def transfer_account(
        self,
        create_user_request: CreateUserRequest,
        account_transfer_request: AccountTransferRequest,
    ):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.ACCOUNT_TRANSFER,
            ResponseSpecs.request_ok(),
        ).post(account_transfer_request)
        return response

    def transfer_account_invalid(
        self,
        create_user_request: CreateUserRequest,
        account_transfer_request: AccountTransferRequest,
    ):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.ACCOUNT_TRANSFER,
            ResponseSpecs.request_bad(),
        ).post(account_transfer_request)
        return response

    def request_credit(
        self, create_user_request: CreateUserRequest, credit_request: CreditRequest
    ):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.request_created(),
        ).post(credit_request)
        return response

    def request_credit_invalid(
        self, create_user_request: CreateUserRequest, credit_request: CreditRequest
    ):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.request_bad(),
        ).post(credit_request)
        return response

    def repay_credit(
        self,
        create_user_request: CreateUserRequest,
        credit_repay_request: CreditRepayRequest,
    ):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.request_ok(),
        ).post(credit_repay_request)
        return response

    def repay_credit_invalid(
        self,
        create_user_request: CreateUserRequest,
        credit_repay_request: CreditRepayRequest,
    ):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.request_unprocessable(),
        ).post(credit_repay_request)
        return response
