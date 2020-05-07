import pytest
import mock
import copy
import json
from httperrors import BadRequestError
from match.views.match_actions.create_match_action import CreateMatchAction
from match.helpers.testing_helpers import get_fake_request
from match.constants.error_codes import (
    REQUIRED_TO_BE_ODD,
)
from match.models.match import Match
from match.models.team import Team
from match.models.set import Set

valid_schema = {
    'sets_number': 5,
    'set_points_number': 25,
    'points_difference': 2,
    'tie_break_points': 15,
    'teams': [
        {
            'name': 'Team one',
            'color': '#ff00ff',
        },
        {
            'name': 'Team two',
            'color': '#ff0000',
        }
    ]
}


@pytest.mark.django_db
class TestCreateMatchActionValidate:

    def test_it_raises_bad_request_when_not_odd_sets_number(self):
        action = CreateMatchAction()
        schema = copy.deepcopy(valid_schema)
        schema['sets_number'] = 4
        request = get_fake_request(body=json.dumps(schema))
        with pytest.raises(BadRequestError) as e:
            action.validate(request)
        assert e.value.error_code == REQUIRED_TO_BE_ODD

    def test_it_does_not_raise_bad_request_when_odd_sets_number(self):
        action = CreateMatchAction()
        request = get_fake_request(body=json.dumps(valid_schema))
        action.validate(request)


@pytest.mark.django_db
class TestCreateMatchActionRun:

    def test_it_create_requested_match_and_teams(self):
        action = CreateMatchAction()
        action.common['body'] = copy.deepcopy(valid_schema)
        request = get_fake_request()
        response = json.loads(action.run(request).content)
        created_matches = Match.objects.all()
        created_teams = Team.objects.filter(match=created_matches[0]).order_by('id')
        created_sets = Set.objects.filter(match_id=created_matches[0].id)

        assert len(response['match']['sets']) == 1
        assert response['match']['sets'][0]['game_status'] == 0
        assert response['match']['sets'][0]['team_one_points'] == 0
        assert response['match']['sets'][0]['team_two_points'] == 0
        assert response['match']['sets'][0]['match_id'] == created_matches[0].id
        assert response['match']['sets'][0]['set_number'] == 1
        assert response['match']['sets'][0]['is_tie_break'] is False
        assert response['match']['sets_number'] == valid_schema['sets_number']
        assert response['match']['set_points_number'] == valid_schema['set_points_number']
        assert response['match']['points_difference'] == valid_schema['points_difference']
        assert response['match']['tie_break_points'] == valid_schema['tie_break_points']
        assert response['match']['token'] == created_matches[0].token
        assert response['match']['teams'][0]['name'] == valid_schema['teams'][0]['name']
        assert response['match']['teams'][0]['color'] == valid_schema['teams'][0]['color']
        assert response['match']['teams'][1]['name'] == valid_schema['teams'][1]['name']
        assert response['match']['teams'][1]['color'] == valid_schema['teams'][1]['color']

        assert created_sets.count() == 1
        assert created_teams.count() == 2
        assert created_matches.count() == 1
        assert created_matches[0].sets_number == valid_schema['sets_number']
        assert created_matches[0].set_points_number == valid_schema['set_points_number']
        assert created_matches[0].points_difference == valid_schema['points_difference']
        assert created_matches[0].tie_break_points == valid_schema['tie_break_points']
        assert created_teams[0].name == valid_schema['teams'][0]['name']
        assert created_teams[0].color == valid_schema['teams'][0]['color']
        assert created_teams[1].name == valid_schema['teams'][1]['name']
        assert created_teams[1].color == valid_schema['teams'][1]['color']

    @mock.patch('match.models.match.Match.generate_access_code')
    def test_atomic_transaction_not_create_partial_match(self, generate_access_code_mock):
        generate_access_code_mock.side_effect = Exception

        action = CreateMatchAction()
        action.common['body'] = copy.deepcopy(valid_schema)
        request = get_fake_request()
        with pytest.raises(Exception):
            action.run(request)

        created_matches = Match.objects.all()
        created_teams = Team.objects.all()

        assert created_teams.count() == 0
        assert created_matches.count() == 0
