import factory
from match.models.match import Match
from match.helpers.date_helpers import get_current_utc_datetime


class MatchFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Match

    status = Match.Status.LIVE.value
    access_code = factory.Sequence(lambda n: 'ABCDS{}'.format(n))
    sets_number = 3
    game_status = Match.GameStatus.PLAYING.value
    set_points_number = 25
    points_difference = 2
    tie_break_points = 15

    created = factory.LazyFunction(get_current_utc_datetime)
    changed = factory.LazyFunction(get_current_utc_datetime)
