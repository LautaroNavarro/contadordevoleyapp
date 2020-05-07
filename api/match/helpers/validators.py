from match.models.match import Match
from httperrors import (
    NotFoundError,
    BadRequestError,

)
from match.constants.error_codes import (
    INVALID_MATCH_ID,
    INVALID_TOKEN,
)
from match.constants.error_messages import (
    RESOURCE_NOT_FOUND_MESSAGE,
    INVALID_TOKEN_MESSAGE
)
from match.constants.entities import MATCH


def validate_token(view, request, *args, **kwargs):
    match = Match.objects.filter(id=kwargs['match_id']).first()
    if not match:
        raise NotFoundError(
            error_message=RESOURCE_NOT_FOUND_MESSAGE.format(MATCH),
            error_code=INVALID_MATCH_ID,
        )
    if 'token' in request.GET.keys():
        if match.token == request.GET.get('token'):
            view.common['match'] = match
            return
    raise BadRequestError(
        error_message=INVALID_TOKEN_MESSAGE,
        error_code=INVALID_TOKEN,
    )
