import string
import random
from django.db import models
from match.helpers.date_helpers import get_current_utc_datetime
from match.models.team import Team
from enum import IntEnum


class Match(models.Model):

    class Status(IntEnum):
        LIVE = 0
        ARCHIVED = 1

    class GameStatus(IntEnum):
        PLAYING = 0
        FINISHED = 1

    status = models.IntegerField(null=False, db_index=True)
    access_code = models.CharField(max_length=255, null=False, db_index=True)

    # Number of sets to play
    sets_number = models.IntegerField(null=False)
    game_status = models.IntegerField(null=False)
    # Points of every set
    set_points_number = models.IntegerField(null=False)
    # Points difference to win
    points_difference = models.IntegerField(null=False)
    # Points of the tie break set
    tie_break_points = models.IntegerField(null=False)

    teams = models.ManyToManyField(Team)

    changed = models.DateTimeField(default=get_current_utc_datetime)
    created = models.DateTimeField(default=get_current_utc_datetime)

    @property
    def team_one(self):
        # TODO: Implement query to get team one
        return None

    @property
    def team_two(self):
        # TODO: Implement query to get team two
        return None

    @property
    def winner_team(self):
        # TODO: Implement query to get winner team
        return None

    @staticmethod
    def generate_access_code(size=7, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    @property
    def serialized(self):
        return {
            'id': self.id,
            'sets_number': self.sets_number,
            'access_code': self.access_code,
            'status': self.status,
            'game_status': self.game_status,
            'set_points_number': self.set_points_number,
            'points_difference': self.points_difference,
            'tie_break_points': self.tie_break_points,
            'sets': [_set.serialized for _set in self.set_set.all()] if self.id else [],
            'teams': [team.serialized for team in Team.objects.filter(match=self)] if self.id else [],
            'winner_team': self.winner_team.serialized if self.winner_team else None,
        }
