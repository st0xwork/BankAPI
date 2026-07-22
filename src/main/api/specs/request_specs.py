import requests

from src.main.api.configs.config import Config
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse


class RequestSpecs:
    @staticmethod
    def base_headers() -> dict[str, str]:
        return {
            "Content-Type": "application/json",
            "accept": "application/json",
        }

    @staticmethod
    def auth_headers(username: str, password: str) -> dict[str, str]:
        login_request = LoginUserRequest(username=username, password=password)
        response = requests.post(
            url=f'{Config.fetch("backendUrl")}/auth/token/login',
            json=login_request.model_dump(),
            headers=RequestSpecs.base_headers(),
        )
        if response.ok:
            login_response = LoginUserResponse.model_validate(response.json())
            headers = RequestSpecs.base_headers()
            headers["Authorization"] = f"Bearer {login_response.token}"
            return headers

        raise RuntimeError(f"Failed to login as {username}: {response.status_code} {response.text}")

    @staticmethod
    def unauth_headers() -> dict[str, str]:
        return RequestSpecs.base_headers()
