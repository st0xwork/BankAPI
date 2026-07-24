import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.login_user_request import LoginUserRequest


@pytest.mark.api
class TestUserLogin:
    def test_login_admin(
            self,
            api_manager: ApiManager,
            admin_login_request: LoginUserRequest
    ):
        response = api_manager.admin_steps.login_user(admin_login_request)

        assert response.user.role == "ROLE_ADMIN", (
            "Авторизованный администратор должен иметь роль ROLE_ADMIN"
        )

        assert response.user.username == admin_login_request.username, (
            "Username должен совпадать с авторизованным пользователем"
        )

    def test_login_user(
            self,
            api_manager: ApiManager,
            created_user_login_request: LoginUserRequest
    ):
        response = api_manager.admin_steps.login_user(created_user_login_request)

        assert response.user.role == "ROLE_USER", (
            "Авторизованный пользователь должен иметь роль ROLE_USER"
        )

        assert response.user.username == created_user_login_request.username, (
            "Username должен совпадать с авторизованным пользователем"
        )
