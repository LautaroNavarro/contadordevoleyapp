import json
from match.views.base.base_action import BaseAction
from django.http import JsonResponse
from match.models.match import Match
from match.models.team import Team
from httperrors import BadRequestError
from match.constants.error_codes import REQUIRED_TO_BE_ODD
from match.constants.error_messages import FIELD_MUST_BE_ODD
from match.schemas.team_schema import create_team_schema
from django.db import transaction


class CreateMatchAction(BaseAction):

    required_body = True

    schema = create_team_schema

    def validate(self, request, *args, **kwargs):
        super().validate(request, *args, **kwargs)
        self.common['body'] = json.loads(request.body)
        if self.common['body']['sets_number'] % 2 == 0:
            raise BadRequestError(
                error_messages=FIELD_MUST_BE_ODD.format('sets_number'),
                error_code=REQUIRED_TO_BE_ODD,
            )

    def run(self, request, *args, **kwargs):
        teams = []
        with transaction.atomic():
            for team in self.common['body']['teams']:
                teams.append(Team.objects.create(**team))
            del self.common['body']['teams']
            self.common['body']['status'] = Match.Status.LIVE.value
            self.common['body']['game_status'] = Match.GameStatus.PLAYING.value
            self.common['body']['access_code'] = Match.generate_access_code()
            self.common['body']['token'] = Match.generate_token()

            match = Match.objects.create(**self.common['body'])
            match.teams.add(*teams)
            match.init_sets()
        match_serialized = match.serialized
        match_serialized['token'] = match.token  # return token one single time
        return JsonResponse({'match': match_serialized})
