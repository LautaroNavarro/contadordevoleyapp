from match.views.base.base_action import BaseAction
from django.http import JsonResponse
from match.models.match import Match
from httperrors import (
    NotFoundError,
    BadRequestError,
)
from match.constants.error_codes import (
    INVALID_ACCESS_CODE,
    REQUIRED_QUERY_PARAM,
)
from match.constants.error_messages import (
    RESOURCE_NOT_FOUND_MESSAGE,
    REQUIRED_QUERY_PARAMETER,
)
from match.constants.entities import MATCH


class SearchMatchAction(BaseAction):

    required_body = False

    def validate(self, request, *args, **kwargs):
        super().validate(request, *args, **kwargs)
        if not request.GET.get('access_code', False):
            raise BadRequestError(
                error_message=REQUIRED_QUERY_PARAMETER.format('access_code'),
                error_code=REQUIRED_QUERY_PARAM,
            )
        match = Match.objects.filter(
            access_code=request.GET.get('access_code'),
            status=Match.Status.LIVE.value,
        ).first()
        if not match:
            raise NotFoundError(
                error_message=RESOURCE_NOT_FOUND_MESSAGE.format(MATCH),
                error_code=INVALID_ACCESS_CODE,
            )
        self.common = {
            'match': match
        }

    def run(self, request, *args, **kwargs):
        return JsonResponse({'match': self.common.get('match').serialized if self.common.get('match') else None})
