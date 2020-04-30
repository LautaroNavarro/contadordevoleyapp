import pytest
import jsonschema
from match.views.base.mappers import json_error_to_http_error_mapper
from httperrors import BadRequestError
from match.constants.error_codes import NOT_A_JSON_BODY


class TestJsonErrorToHttpErrorMapper:

    def test_catch_bad_request_error_and_return_json_response(self):
        @json_error_to_http_error_mapper
        def get_think():
            raise jsonschema.exceptions.ValidationError('Invalid field error')
        with pytest.raises(BadRequestError) as e:
            get_think()
        assert e.value.error_message == 'Invalid field error'
        assert e.value.error_code == NOT_A_JSON_BODY
