import pytest
import json
from httperrors import (
    NotFoundError,
    BadRequestError,
)
from match.views.match_actions.match_controls_action import MatchControlsAction
from match.helpers.testing_helpers import get_fake_request
from match.constants.error_codes import (
    INVALID_MATCH_ID,
    INVALID_TEAM_SELECTION,
    INVALID_MATCH_STATUS,
)
from match.tests.factories.match_factory import MatchFactory
from match.tests.factories.team_factory import TeamFactory
from match.models.match import Match
from match.models.team import Team
from match.models.set import Set


@pytest.mark.django_db
class TestMatchControlsActionValidate:

    def test_it_raises_not_found_when_invalid_id(self):
        action = MatchControlsAction()
        request = get_fake_request()
        with pytest.raises(NotFoundError) as e:
            action.validate(request, match_id=1, team='team_one')
        assert e.value.error_code == INVALID_MATCH_ID

    def test_it_raises_invalid_when_invalid_team(self):
        action = MatchControlsAction()
        request = get_fake_request()
        match = MatchFactory()
        with pytest.raises(BadRequestError) as e:
            action.validate(request, match_id=match.id, team='no_existing_team')
        assert e.value.error_code == INVALID_TEAM_SELECTION

    def test_it_raises_invalid_when_invalid_game_status(self):
        action = MatchControlsAction()
        request = get_fake_request()
        match = MatchFactory(game_status=Match.GameStatus.FINISHED.value)
        with pytest.raises(BadRequestError) as e:
            action.validate(request, match_id=match.id, team='team_one')
        assert e.value.error_code == INVALID_MATCH_STATUS

    def test_it_does_not_raise_invalid_when_valid_request(self):
        action = MatchControlsAction()
        request = get_fake_request()
        match = MatchFactory()
        action.validate(request, match_id=match.id, team='team_one')

@pytest.mark.django_db
class TestMatchControlsActionRun:

    def test_it_add_one_to_the_correct_team_response_and_db(self):
        action = MatchControlsAction()
        request = get_fake_request()
        match = MatchFactory()
        match.teams.add(*[TeamFactory() for i in range(2)])
        match.init_sets()
        action.common['match'] = match
        response = json.loads(action.run(request=request, match_id=match.id, team='team_one').content)
        sets = Set.objects.filter(match_id=match.id)

        assert len(response['match']['sets']) == 1
        assert response['match']['sets'][0]['game_status'] == Set.GameStatus.PLAYING.value
        assert response['match']['sets'][0]['team_one_points'] == 1
        assert response['match']['sets'][0]['team_two_points'] == 0
        assert response['match']['sets'][0]['match_id'] == match.id
        assert response['match']['sets'][0]['set_number'] == 1
        assert response['match']['sets'][0]['is_tie_break'] is False

        assert response['match']['sets_number'] == match.sets_number
        assert response['match']['set_points_number'] == match.set_points_number
        assert response['match']['points_difference'] == match.points_difference
        assert response['match']['tie_break_points'] == match.tie_break_points
        assert response['match']['teams'][0]['name'] == match.teams.all()[0].name
        assert response['match']['teams'][0]['color'] == match.teams.all()[0].color
        assert response['match']['teams'][1]['name'] == match.teams.all()[1].name
        assert response['match']['teams'][1]['color'] == match.teams.all()[1].color

        match_db = Match.objects.get(id=match.id)

        assert sets.count() == 1
        assert match_db.sets_number == match.sets_number
        assert match_db.set_points_number == match.set_points_number
        assert match_db.points_difference == match.points_difference
        assert match_db.tie_break_points == match.tie_break_points
        assert match_db.game_status == Match.GameStatus.PLAYING.value
        assert len(sets) == 1
        assert sets[0].game_status == Set.GameStatus.PLAYING.value
        assert sets[0].team_one_points == 1
        assert sets[0].team_two_points == 0

    def test_it_add_one_to_the_team_two_response_and_db(self):
        action = MatchControlsAction()
        request = get_fake_request()
        match = MatchFactory()
        match.teams.add(*[TeamFactory() for i in range(2)])
        match.init_sets()
        action.common['match'] = match
        response = json.loads(action.run(request=request, match_id=match.id, team='team_two').content)
        sets = Set.objects.filter(match_id=match.id)

        assert len(response['match']['sets']) == 1
        assert response['match']['sets'][0]['game_status'] == Set.GameStatus.PLAYING.value
        assert response['match']['sets'][0]['team_one_points'] == 0
        assert response['match']['sets'][0]['team_two_points'] == 1
        assert response['match']['sets'][0]['match_id'] == match.id
        assert response['match']['sets'][0]['set_number'] == 1
        assert response['match']['sets'][0]['is_tie_break'] is False

        assert response['match']['sets_number'] == match.sets_number
        assert response['match']['set_points_number'] == match.set_points_number
        assert response['match']['points_difference'] == match.points_difference
        assert response['match']['tie_break_points'] == match.tie_break_points
        assert response['match']['teams'][0]['name'] == match.teams.all()[0].name
        assert response['match']['teams'][0]['color'] == match.teams.all()[0].color
        assert response['match']['teams'][1]['name'] == match.teams.all()[1].name
        assert response['match']['teams'][1]['color'] == match.teams.all()[1].color

        match_db = Match.objects.get(id=match.id)

        assert sets.count() == 1
        assert match_db.sets_number == match.sets_number
        assert match_db.set_points_number == match.set_points_number
        assert match_db.points_difference == match.points_difference
        assert match_db.tie_break_points == match.tie_break_points
        assert match_db.game_status == Match.GameStatus.PLAYING.value
        assert len(sets) == 1
        assert sets[0].game_status == Set.GameStatus.PLAYING.value
        assert sets[0].team_one_points == 0
        assert sets[0].team_two_points == 1

    # def test_it_add_one_to_the_correct_team_and_create_new_set_when_game_is_not_finished(self):
    #     action = MatchControlsAction()
    #     request = get_fake_request()
    #     match = MatchFactory()
    #     match.teams.add(*[TeamFactory() for i in range(2)])
    #     match.init_sets()
    #     sets = Set.objects.filter(match_id=match.id)
    #     sets[0].team_one_points == 24
    #     sets[0].save()
    #     action.common['match'] = match
    #     action.run(request=request, match_id=match.id, team='team_one')
    #     sets = Set.objects.filter(match_id=match.id)
    #     assert len(sets) == 2

