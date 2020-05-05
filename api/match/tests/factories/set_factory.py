import factory
from match.models.set import Set
from match.helpers.date_helpers import get_current_utc_datetime
from match.models.match import Match


class SetFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Set

    game_status = Set.GameStatus.PLAYING.value
    team_one_points = 0
    team_two_points = 0
    match = factory.SubFactory(Match)
    set_number = 0
    is_tie_break = False

    created = factory.LazyFunction(get_current_utc_datetime)
    changed = factory.LazyFunction(get_current_utc_datetime)

class SetFinishedTeamOneFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Set

    game_status = Set.GameStatus.FINISHED.value
    team_one_points = 25
    team_two_points = 0
    match = factory.SubFactory(Match)
    set_number = 0
    is_tie_break = False

    created = factory.LazyFunction(get_current_utc_datetime)
    changed = factory.LazyFunction(get_current_utc_datetime)


class SetFinishedTeamTwoFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Set

    game_status = Set.GameStatus.FINISHED.value
    team_one_points = 0
    team_two_points = 25
    match = factory.SubFactory(Match)
    set_number = 0
    is_tie_break = False

    created = factory.LazyFunction(get_current_utc_datetime)
    changed = factory.LazyFunction(get_current_utc_datetime)
