import pytest

from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.login_user_request import LoginUserRequest


@pytest.fixture
def create_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request


@pytest.fixture
def credit_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest).model_copy(
        update={
            "role": "ROLE_CREDIT_SECRET"
        }
    )

    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def invalid_create_user_request(request):
    invalid_data = request.param

    user_request = RandomModelGenerator.generate(CreateUserRequest).model_copy(
        update=invalid_data
    )

    return user_request

@pytest.fixture
def created_user_login_request(create_user_request: CreateUserRequest):
    user_request = LoginUserRequest(
        username=create_user_request.username,
        password=create_user_request.password
    )

    return user_request