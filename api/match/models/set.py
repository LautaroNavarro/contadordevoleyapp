from django.db import models
from match.helpers.date_helpers import get_current_utc_datetime
from enum import IntEnum


class Set(models.Model):

    class GameStatus(IntEnum):
        PLAYING = 1
        FINISHED = 2

    game_status = models.IntegerField(null=False, db_index=True)
    team_one_points = models.IntegerField(null=False)
    team_two_points = models.IntegerField(null=False)
    match = models.ForeignKey('Match', on_delete=models.CASCADE, null=False)
    set_number = models.IntegerField(null=False)
    is_tie_break = models.BooleanField(default=False)

    changed = models.DateTimeField(default=get_current_utc_datetime)
    created = models.DateTimeField(default=get_current_utc_datetime)

    @property
    def serialized(self):
        return {
            'id': self.id,
            'game_status': self.game_status,
            'team_one_points': self.team_one_points,
            'team_two_points': self.team_two_points,
            'match_id': self.match_id,
            'set_number': self.set_number,
            'is_tie_break': self.is_tie_break,
        }
