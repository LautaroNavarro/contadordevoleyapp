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
    INVALID_SET_STATUS,
)
from match.constants.error_messages import (
    RESOURCE_NOT_FOUND_MESSAGE,
    TEAM_NOT_ONE_OF,
    MATCH_IS_FINISHED,
    CAN_NOT_SUBSCRACT_POINTS,
)
from match.constants.entities import MATCH
from match.helpers.validators import validate_token


class SubPointsAction(BaseAction):
    """
    This action handle substracting points for the counter of a team
    """
    required_body = False

    VALID_TEAMS = ['team_one', 'team_two']

    validators = [validate_token]

    def validate(self, request, match_id, team, *args, **kwargs):
        kwargs['match_id'] = match_id
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
        if not match.can_substract_points(team):
            raise BadRequestError(
                error_message=CAN_NOT_SUBSCRACT_POINTS,
                error_code=INVALID_SET_STATUS,
            )
        self.common = {
            'match': match
        }

    def run(self, request, match_id, team, *args, **kwargs):
        self.common['match'].sub_team_counter(team)
        return JsonResponse({'match': self.common.get('match').serialized if self.common.get('match') else None})
