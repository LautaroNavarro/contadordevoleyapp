from django.db import models
from match.helpers.date_helpers import get_current_utc_datetime
from match.models.team import Team


class Match(models.Model):

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
        return False

    @property
    def team_two(self):
        # TODO: Implement query to get team two
        return False

    @property
    def winner_team(self):
        # TODO: Implement query to get winner team
        return False

    @property
    def serialized(self):
        return {
            'sets_number': self.sets_number,
            'access_code': self.access_code,
            'status': self.status,
            'game_status': self.game_status,
            'sets_points_number': self.sets_points_number,
            'points_difference': self.points_difference,
            'tie_break_points': self.tie_break_points,
            'team_one': self.team_one.serialized if self.team_one else None,
            'team_two': self.team_two.serialized if self.team_two else None,
            'winner_team': self.winner_team.serialized if self.winner_team else None,
        }
