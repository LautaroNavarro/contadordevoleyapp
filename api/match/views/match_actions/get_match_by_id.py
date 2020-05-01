from match.views.base.base_action import BaseAction
from django.http import JsonResponse
from match.models.match import Match
from httperrors import NotFoundError
from match.constants.error_codes import INVALID_MATCH_ID
from match.constants.error_messages import RESOURCE_NOT_FOUND_MESSAGE
from match.constants.entities import MATCH


class GetMatchByIdAction(BaseAction):

    required_body = False

    def validate(self, request, match_id, *args, **kwargs):
        super().validate(request, *args, **kwargs)
        match = Match.objects.filter(id=match_id).first()
        if not match:
            raise NotFoundError(
                error_message=RESOURCE_NOT_FOUND_MESSAGE.format(MATCH),
                error_code=INVALID_MATCH_ID,
            )
        self.common = {
            'match': match
        }

    def run(self, request, match_id, *args, **kwargs):
        return JsonResponse({'match': self.common.get('match').serialized if self.common.get('match') else None})
