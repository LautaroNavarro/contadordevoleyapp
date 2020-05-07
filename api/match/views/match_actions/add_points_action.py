from match.views.base.base_action import BaseAction
from django.http import JsonResponse
from httperrors import (
    BadRequestError,
)
from match.constants.error_codes import (
    INVALID_TEAM_SELECTION,
    INVALID_MATCH_STATUS,
)
from match.constants.error_messages import (
    TEAM_NOT_ONE_OF,
    MATCH_IS_FINISHED,
)
from match.helpers.validators import validate_token


class AddPointsAction(BaseAction):
    """
    This action handle adding points to the counter of a team
    """
    required_body = False

    VALID_TEAMS = ['team_one', 'team_two']

    validators = [validate_token]

    def validate(self, request, match_id, team, *args, **kwargs):
        kwargs['match_id'] = match_id
        super().validate(request, *args, **kwargs)
        if not self.common['match'].is_operable_match():
            raise BadRequestError(
                error_message=MATCH_IS_FINISHED,
                error_code=INVALID_MATCH_STATUS,
            )
        if team not in self.VALID_TEAMS:
            raise BadRequestError(
                error_message=TEAM_NOT_ONE_OF.format(','.join(self.VALID_TEAMS)),
                error_code=INVALID_TEAM_SELECTION,
            )

    def run(self, request, match_id, team, *args, **kwargs):
        self.common['match'].add_team_counter(team)
        return JsonResponse({'match': self.common.get('match').serialized if self.common.get('match') else None})
