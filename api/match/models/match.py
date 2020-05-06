import string
import random
from django.db import models
from match.helpers.date_helpers import get_current_utc_datetime
from match.models.team import Team
from match.models.set import Set
from enum import IntEnum
from math import floor
from django.db import transaction


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
        return Team.objects.filter(match=self).order_by('id').first()

    @property
    def team_two(self):
        return Team.objects.filter(match=self).order_by('-id').first()

    def get_counters(self):
        sets = self.set_set.all()
        team_one_sets_counter = 0
        team_two_sets_counter = 0
        for _set in sets:
            if _set.game_status == Set.GameStatus.FINISHED.value:
                if _set.team_one_points > _set.team_two_points:
                    team_one_sets_counter += 1
                else:
                    team_two_sets_counter += 1
        return team_one_sets_counter, team_two_sets_counter

    @property
    def winner_team(self):
        team_one_sets_counter, team_two_sets_counter = self.get_counters()
        if (
            team_one_sets_counter >= self.get_minimum_sets_to_play()
        ):
            return self.team_one
        elif team_two_sets_counter >= self.get_minimum_sets_to_play():
            return self.team_two
        return None

    @staticmethod
    def generate_access_code(size=7, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def get_minimum_sets_to_play(self):
        return floor(self.sets_number / 2) + 1

    def init_sets(self):
        Set.objects.create(
            game_status=Set.GameStatus.PLAYING.value,
            team_one_points=0,
            team_two_points=0,
            match=self,
            set_number=1,
            is_tie_break=False,
        )

    def get_current_set(self):
        return Set.objects.filter(
            match=self,
            game_status=Set.GameStatus.PLAYING.value,
        ).first()

    def add_team_counter(self, team):
        current_set = self.get_current_set()

        setattr(current_set, '{}_points'.format(team), getattr(current_set, '{}_points'.format(team)) + 1)

        with transaction.atomic():
            current_set.save()
            self.update_game_status()

    def sub_team_counter(self, team):
        current_set = self.get_current_set()
        setattr(current_set, '{}_points'.format(team), getattr(current_set, '{}_points'.format(team)) - 1)
        current_set.save()

    def get_target_points(self, is_tie_break):
        if is_tie_break:
            return self.tie_break_points
        return self.set_points_number

    def new_set_should_be_tie_break(self):
        team_one_sets_counter, team_two_sets_counter = self.get_counters()
        return (
            (team_one_sets_counter == team_two_sets_counter)
            and (team_one_sets_counter + team_two_sets_counter) == (self.sets_number - 1)
        )

    def get_played_set_count(self):
        return self.set_set.all().count()

    def update_game_status(self):
        create_new_set = False
        for _set in self.set_set.all():
            if _set.game_status == Set.GameStatus.PLAYING.value:
                if (
                    (
                        _set.team_one_points >= self.get_target_points(_set.is_tie_break) and (
                            _set.team_one_points - _set.team_two_points
                        ) >= self.points_difference
                    )
                    or (
                        _set.team_two_points >= self.get_target_points(_set.is_tie_break) and (
                            _set.team_two_points - _set.team_one_points
                        ) >= self.points_difference
                    )
                ):
                    _set.game_status = Set.GameStatus.FINISHED.value
                    _set.save()
                    create_new_set = True

        if self.is_match_game_status_finished():
            self.game_status = self.GameStatus.FINISHED.value
            self.save()
        elif create_new_set:
            Set.objects.create(
                game_status=Set.GameStatus.PLAYING.value,
                team_one_points=0,
                team_two_points=0,
                match=self,
                set_number=self.get_played_set_count() + 1,
                is_tie_break=self.new_set_should_be_tie_break()
            )

    def is_match_game_status_finished(self):
        team_one_sets_counter, team_two_sets_counter = self.get_counters()
        if (
            team_one_sets_counter >= self.get_minimum_sets_to_play()
            or team_two_sets_counter >= self.get_minimum_sets_to_play()
        ):
            return True
        return False

    def can_substract_points(self, team):
        current_set = self.get_current_set()
        if current_set:
            team_points = getattr(current_set, '{}_points'.format(team))
            return team_points > 0
        return False

    def is_operable_match(self):
        return self.game_status != self.GameStatus.FINISHED.value

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
