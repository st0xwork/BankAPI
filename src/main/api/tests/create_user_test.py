import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.user_crud import UserCrudDb as User
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestCreateUser:
    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)],
        ids=["generated-user"],
    )
    def test_create_user_valid(
        self,
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
        db_session: Session,
    ):
        response = api_manager.admin_steps.create_user(create_user_request)

        assert create_user_request.username == response.username
        assert create_user_request.role == response.role

        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db.username == create_user_request.username, (
            "Созданного пользователя нет в базе"
        )

    @pytest.mark.parametrize(
        "invalid_data",
        [
            {"username": "абв"},
            {"username": "ab"},
            {"username": "abv!"},
            {"password": "Pas!sw0rд"},
            {"password": "Pas!sw0"},
            {"password": "pas!sw0rd"},
            {"password": "PAS!SW0RD"},
            {"password": "Passw0rd"},
            {"password": "Pas!swrd"},
        ],
        ids=[
            "username-cyrillic",
            "username-too-short",
            "username-special-character",
            "password-cyrillic",
            "password-too-short",
            "password-without-uppercase",
            "password-without-lowercase",
            "password-without-special-character",
            "password-without-digit",
        ],
    )
    def test_create_user_invalid(self, db_session: Session, invalid_data, api_manager: ApiManager):
        create_user_request = RandomModelGenerator.generate(CreateUserRequest).model_copy(update=invalid_data)

        api_manager.admin_steps.create_user_invalid(create_user_request)

        user_from_db = User.get_user_by_username(db_session, create_user_request.username)

        assert user_from_db is None, "Пользователь создан, ошибка"
