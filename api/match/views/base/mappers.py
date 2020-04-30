import jsonschema

from httperrors import BadRequestError
from match.constants.error_codes import NOT_A_JSON_BODY


def json_error_to_http_error_mapper(validate_request_schema):
    """
    Use this decorator to map json validation error to request error
    """
    def wrapper(*args, **kwargs):
        try:
            return validate_request_schema(*args, **kwargs)
        except jsonschema.exceptions.ValidationError as error:
            raise BadRequestError(
                error_message=error.message,
                error_code=NOT_A_JSON_BODY,
            )
    return wrapper
