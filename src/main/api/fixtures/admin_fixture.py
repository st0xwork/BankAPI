import pytest

from src.main.api.configs.config import Config
from src.main.api.models.login_user_request import LoginUserRequest


@pytest.fixture
def admin_login_request():
    return LoginUserRequest(
        username=Config.fetch("adminUsername", "admin"),
        password=Config.require("adminPassword"),
    )
