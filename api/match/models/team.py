from django.db import models
from match.helpers.date_helpers import get_current_utc_datetime


class Team(models.Model):

    name = models.CharField(max_length=255, null=False)
    color = models.CharField(max_length=7, null=False, blank=False)
    changed = models.DateTimeField(default=get_current_utc_datetime)
    created = models.DateTimeField(default=get_current_utc_datetime)

    @property
    def serialized(self):
        return {
            'id': self.id,
            'name': self.name,
            'color': self.color,
        }
