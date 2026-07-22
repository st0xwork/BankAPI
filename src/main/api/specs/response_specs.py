from collections.abc import Callable
from http import HTTPStatus

from requests import Response


class ResponseSpecs:
    @staticmethod
    def _status(expected_status: HTTPStatus) -> Callable[[Response], None]:
        def confirm(response: Response) -> None:
            assert response.status_code == expected_status, response.text

        return confirm

    @staticmethod
    def request_ok() -> Callable[[Response], None]:
        return ResponseSpecs._status(HTTPStatus.OK)

    @staticmethod
    def request_created() -> Callable[[Response], None]:
        return ResponseSpecs._status(HTTPStatus.CREATED)

    @staticmethod
    def request_bad() -> Callable[[Response], None]:
        return ResponseSpecs._status(HTTPStatus.BAD_REQUEST)

    @staticmethod
    def request_unprocessable() -> Callable[[Response], None]:
        return ResponseSpecs._status(HTTPStatus.UNPROCESSABLE_ENTITY)

