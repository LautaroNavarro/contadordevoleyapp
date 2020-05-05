import factory
from match.models.match import Team
from match.helpers.date_helpers import get_current_utc_datetime


class TeamFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Team

    name = factory.Sequence(lambda n: 'name{}'.format(n))
    color = '#ff0000'

    created = factory.LazyFunction(get_current_utc_datetime)
    changed = factory.LazyFunction(get_current_utc_datetime)
