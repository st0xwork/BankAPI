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

        assert create_user_request.username == response.username, (
            "Username в ответе не совпадает с отправленным Username"
        )
        assert create_user_request.role == response.role, (
            "Роль пользователя в ответе не совпадает с отправленной ролью"
        )

        user_from_db = User.get_user_by_username(db_session, create_user_request.username)

        assert user_from_db.username == create_user_request.username, (
            "Созданного пользователя нет в базе"
        )

    @pytest.mark.parametrize(
        "invalid_create_user_request",
        [
          pytest.param(
              {"username": "абв"},
              id="invalid-username",
          ),
          pytest.param(
              {"password": "Pas!sw0"},
              id="invalid-password",
          ),
        ],
        indirect=True
    )
    def test_create_user_invalid(
            self, db_session: Session,
            invalid_create_user_request: CreateUserRequest,
            api_manager: ApiManager
    ):

        api_manager.admin_steps.create_user_invalid(invalid_create_user_request)

        user_exists = User.user_exists(db_session, invalid_create_user_request.username)

        assert not user_exists, "Пользователь с невалидными данными появился в базе"