from match.views.base.base_action import BaseAction
from match.constants.error_codes import INVALID_PAGE
from httperrors import BadRequestError
from match.views.base.handlers import (
    request_error_handler,
    json_error_handler,
)


class PaginatedBaseAction(BaseAction):

    def validate(self, request, *args, **kwargs):
        super().validate(request, *args, **kwargs)
        if request.GET.get('page', False) is not False and request.GET.get('page') < 1:
            raise BadRequestError(
                error_message='Page number must be positive',
                error_code=INVALID_PAGE,
            )

    @json_error_handler
    @request_error_handler
    def __call__(self, request, *args, **kwargs):
        self.validate(request, *args, **kwargs)
        return self.run(request, int(request.GET.get('page', 1)), *args, **kwargs)
