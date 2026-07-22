import logging
from typing import Any

import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_response import CreateUserResponse


@pytest.fixture
def created_obj():
    objects: list[Any] = []
    yield objects
    clean_user(objects)


def clean_user(objects: list[Any]):
    api_manager = ApiManager(objects)
    for created_object in reversed(objects):
        if isinstance(created_object, CreateUserResponse):
            api_manager.admin_steps.delete_user(created_object.id)
        else:
            logging.warning("Unsupported object in cleanup: %r", created_object)
