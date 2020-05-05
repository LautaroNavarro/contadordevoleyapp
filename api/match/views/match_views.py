from django.views import View
from match.views.match_actions.get_match_by_id import GetMatchByIdAction
from match.views.match_actions.search_match_action import SearchMatchAction
from match.views.match_actions.match_controls_action import MatchControlsAction


class MatchByIdView(View):

    def get(self, request, *args, **kwargs):
        action = GetMatchByIdAction()
        return action(request, *args, **kwargs)


class MatchControls(View):

    def post(self, request, *args, **kwargs):
        action = MatchControlsAction()
        return action(request, *args, **kwargs)


class SearchMatchView(View):

    def get(self, request, *args, **kwargs):
        action = SearchMatchAction()
        return action(request, *args, **kwargs)
