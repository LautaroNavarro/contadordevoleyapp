import json
from match.views.base.handlers import (
    request_error_handler,
    json_error_handler,
)
from httperrors import BadRequestError
from django.http import JsonResponse


class TestRequestErrorHandler:

    def test_catch_bad_request_error_and_return_json_response(self):
        @request_error_handler
        def get_think():
            raise BadRequestError(
                error_message='Invalid field error',
                error_code='SOME_ERROR_CODE',
            )

        json_response = get_think()
        assert isinstance(json_response, JsonResponse)
        assert json_response.status_code == 400
        assert json_response.content == b'{"error_message": "Invalid field error", "status_code": 400}'


class TestJsonErrorHandler:

    def test_catch_json_error_and_return_json_response(self):
        @json_error_handler
        def get_think():
            json.loads('{')

        json_response = get_think()
        assert isinstance(json_response, JsonResponse)
        assert json_response.status_code == 400
        assert json_response.content == b'{"error_message": "Not a json body", "status_code": 400}'
