from django.urls import path
from match.views.match_views import (
    MatchByIdView,
    SearchMatchView,
)

urlpatterns = [
    path('matches/<int:match_id>', MatchByIdView.as_view()),
    path('matches/search/', SearchMatchView.as_view()),
]
