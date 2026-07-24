import pytest

from src.main.api.models.login_user_request import LoginUserRequest

@pytest.fixture

def admin_login_request():
    return LoginUserRequest(
        username="admin",
        password="123456",
    )