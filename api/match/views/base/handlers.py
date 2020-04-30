from json.decoder import JSONDecodeError
from django.http import JsonResponse
from httperrors import (
    RequestError,
    BadRequestError,
)
from match.constants.error_codes import NOT_A_JSON_BODY


def get_json_response_from_http_error(httpError):
    return JsonResponse(
        status=httpError.status_code,
        data=httpError.serialize(),
    )


def json_error_handler(run):
    """
    Use this decorator to catch json errors
    """
    def wrapper(*args, **kwargs):
        try:
            return run(*args, **kwargs)
        except JSONDecodeError:

            return get_json_response_from_http_error(BadRequestError(
                error_message='Not a json body',
                error_code=NOT_A_JSON_BODY,
            ))
    return wrapper


def request_error_handler(run):
    """
    Use this decorator to catch request errors
    """
    def wrapper(*args, **kwargs):
        try:
            return run(*args, **kwargs)
        except RequestError as error:
            return get_json_response_from_http_error(error)
    return wrapper
