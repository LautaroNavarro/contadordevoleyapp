from django.urls import path
from match.views.match_views import (
    MatchByIdView,
    SearchMatchView,
    AddPointsView,
    SubPointsView,
    MatchesView,
)

urlpatterns = [
    path('matches/', MatchesView.as_view()),
    path('matches/<int:match_id>', MatchByIdView.as_view()),
    path('matches/<int:match_id>/<str:team>/add', AddPointsView.as_view()),
    path('matches/<int:match_id>/<str:team>/sub', SubPointsView.as_view()),
    path('matches/search/', SearchMatchView.as_view()),
]
