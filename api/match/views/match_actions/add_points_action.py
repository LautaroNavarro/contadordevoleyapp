from match.views.base.base_action import BaseAction
from django.http import JsonResponse
from match.models.match import Match
from httperrors import (
    NotFoundError,
    BadRequestError,

)
from match.constants.error_codes import (
    INVALID_MATCH_ID,
    INVALID_TEAM_SELECTION,
    INVALID_MATCH_STATUS,
)
from match.constants.error_messages import (
    RESOURCE_NOT_FOUND_MESSAGE,
    TEAM_NOT_ONE_OF,
    MATCH_IS_FINISHED,
)
from match.constants.entities import MATCH


class AddPointsAction(BaseAction):
    """
    This action handle adding points to the counter of a team
    """
    required_body = False

    VALID_TEAMS = ['team_one', 'team_two']

    def validate(self, request, match_id, team, *args, **kwargs):
        super().validate(request, *args, **kwargs)
        match = Match.objects.filter(id=match_id).first()
        if not match:
            raise NotFoundError(
                error_message=RESOURCE_NOT_FOUND_MESSAGE.format(MATCH),
                error_code=INVALID_MATCH_ID,
            )
        if not match.is_operable_match():
            raise BadRequestError(
                error_message=MATCH_IS_FINISHED,
                error_code=INVALID_MATCH_STATUS,
            )
        if team not in self.VALID_TEAMS:
            raise BadRequestError(
                error_message=TEAM_NOT_ONE_OF.format(','.join(self.VALID_TEAMS)),
                error_code=INVALID_TEAM_SELECTION,
            )
        self.common = {
            'match': match
        }

    def run(self, request, match_id, team, *args, **kwargs):
        self.common['match'].add_team_counter(team)
        return JsonResponse({'match': self.common.get('match').serialized if self.common.get('match') else None})
