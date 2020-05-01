import json
import pytest
import mock
from match.views.base.base_action import BaseAction
from httperrors import BadRequestError


class TestBaseAction:

    class TestValidateRequestContentTypeMethod:

        def test_not_raise_error_if_not_setted_content_type(self):
            action = BaseAction()
            request = mock.Mock()
            action.validate_request_content_type(request)

        def test_not_raise_error_if_correct_content_type(self):
            action = BaseAction()
            action.content_type = 'application/json'
            request = mock.Mock()
            request.content_type = 'application/json'
            action.validate_request_content_type(request)

        def test_raise_error_if_not_correct_content_type(self):
            action = BaseAction()
            action.content_type = 'application/json'
            request = mock.Mock()
            request.content_type = 'some/content_type'
            with pytest.raises(BadRequestError):
                action.validate_request_content_type(request)

    class TestValidateRequestSchema:

        def test_not_raise_errr_if_not_required_body_and_no_body(self):
            action = BaseAction()
            action.required_body = False
            request = mock.Mock()
            request.body = None
            action.validate_request_schema(request)

        def test_raise_error_if_required_body_and_no_body(self):
            action = BaseAction()
            action.required_body = True
            request = mock.Mock()
            request.body = None
            with pytest.raises(BadRequestError):
                action.validate_request_schema(request)

        def test_not_it_do_not_validate_schema_if_not_requested_schema(self):
            action = BaseAction()
            action.schema = None
            request = mock.Mock()
            request.body = {}
            action.validate_request_schema(request)

        def test_it_validate_schema_if_requested_schema_invalid_schema(self):
            action = BaseAction()
            action.schema = {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                    },
                },
                "additionalProperties": False,
            }
            request = mock.Mock()
            request.body = json.dumps({'name': 1})
            with pytest.raises(BadRequestError):
                action.validate_request_schema(request)

        def test_it_validate_schema_if_requested_schema_valid_schema(self):
            action = BaseAction()
            action.schema = {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                    },
                },
                "additionalProperties": False,
            }
            request = mock.Mock()
            request.body = json.dumps({'name': '1'})
            action.validate_request_schema(request)
