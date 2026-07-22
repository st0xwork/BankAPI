import allure
from typing import Any, Optional

from src.main.api.configs.config import Config
from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.http_requester import HttpRequester
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.models.base_model import BaseModel


class ValidateCrudRequester(HttpRequester):
    def __init__(self, request_spec, endpoint: Endpoint, response_spec):
        super().__init__(request_spec, endpoint, response_spec)
        self.crud_requester = CrudRequester(
            request_spec=request_spec, endpoint=endpoint, response_spec=response_spec
        )

    def post(self, model: Optional[BaseModel] | None) -> Optional[BaseModel]:
        response = self.crud_requester.post(model)
        with allure.step(
            f'POST {Config.fetch("backendURL")}{self.endpoint.value.url} and Validated Model'
        ):
            allure.attach(
                f"Validated Model response: {self.endpoint.value.response_model.__name__}"
            )

        response_model = self.endpoint.value.response_model
        if response_model is None:
            raise ValueError(f"Response model is not configured for {self.endpoint.name}")
        return response_model.model_validate(response.json())

    def delete(self, user_id: int) -> Any:
        return self.crud_requester.delete(user_id)
