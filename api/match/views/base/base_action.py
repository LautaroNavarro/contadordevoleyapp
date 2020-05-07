import json
from jsonschema import validate as validate_request
from match.views.base.handlers import (
    request_error_handler,
    json_error_handler,
)

from match.views.base.mappers import json_error_to_http_error_mapper
from httperrors import BadRequestError


class BaseAction():

    content_type = None

    schema = None

    required_body = False

    common = {}

    validators = []

    @json_error_handler
    @request_error_handler
    def __call__(self, request, *args, **kwargs):
        self.validate(request, *args, **kwargs)
        return self.run(request, *args, **kwargs)

    def validate(self, request, *args, **kwargs):
        self.validate_request_content_type(request)
        self.validate_request_schema(request)
        for validator in self.validators:
            validator(self, request, *args, **kwargs)

    @json_error_to_http_error_mapper
    def validate_request_schema(self, request):
        if self.required_body and not request.body:
            raise BadRequestError('You must pass a body')
        if self.schema:
            request_params = json.loads(request.body)
            validate_request(instance=request_params, schema=self.schema)

    def validate_request_content_type(self, request):
        if self.content_type:
            if not request.content_type == self.content_type:
                raise BadRequestError('Content type must be {}.'.format(self.content_type))
