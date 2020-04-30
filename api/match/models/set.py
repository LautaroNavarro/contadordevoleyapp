from django.db import models
from match.helpers.date_helpers import get_current_utc_datetime
from match.models.match import Match


class Set(models.Model):

    status = models.IntegerField(null=False, db_index=True)
    team_one_points = models.IntegerField(null=False)
    team_two_points = models.IntegerField(null=False)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, null=False)
    set_number = models.IntegerField(null=False)
    is_tie_break = models.BooleanField(default=False)

    changed = models.DateTimeField(default=get_current_utc_datetime)
    created = models.DateTimeField(default=get_current_utc_datetime)

    @property
    def serialized(self):
        return {
            'status': self.status,
            'team_one_points': self.game_status,
            'team_two_points': self.sets_points_number,
            'match_id': self.match_id,
            'set_number': self.set_number,
            'is_tie_break': self.is_tie_break,
        }
