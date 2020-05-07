from django.views import View
from match.views.match_actions.get_match_by_id import GetMatchByIdAction
from match.views.match_actions.search_match_action import SearchMatchAction
from match.views.match_actions.add_points_action import AddPointsAction
from match.views.match_actions.sub_points_action import SubPointsAction
from match.views.match_actions.create_match_action import CreateMatchAction


class MatchByIdView(View):

    def get(self, request, *args, **kwargs):
        action = GetMatchByIdAction()
        return action(request, *args, **kwargs)


class MatchesView(View):
    def post(self, request, *args, **kwargs):
        action = CreateMatchAction()
        return action(request, *args, **kwargs)


class AddPointsView(View):

    def post(self, request, *args, **kwargs):
        action = AddPointsAction()
        return action(request, *args, **kwargs)


class SubPointsView(View):

    def post(self, request, *args, **kwargs):
        action = SubPointsAction()
        return action(request, *args, **kwargs)


class SearchMatchView(View):

    def get(self, request, *args, **kwargs):
        action = SearchMatchAction()
        return action(request, *args, **kwargs)
