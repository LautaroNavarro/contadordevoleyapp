import pytest
import json
from httperrors import NotFoundError
from match.views.match_actions.get_match_by_id import GetMatchByIdAction
from match.helpers.testing_helpers import get_fake_request
from match.constants.error_codes import INVALID_MATCH_ID
from match.tests.factories.match_factory import MatchFactory


@pytest.mark.django_db
class TestGetMatchByIdActionValidate:

    def test_it_raises_not_found_when_invalid_id(self):
        action = GetMatchByIdAction()
        request = get_fake_request()
        with pytest.raises(NotFoundError) as e:
            action.validate(request, match_id=1)
        assert e.value.error_code == INVALID_MATCH_ID

    def test_it_does_not_raise_error_when_valid_id_and_write_match_in_common(self):
        action = GetMatchByIdAction()
        match = MatchFactory()
        request = get_fake_request()
        action.validate(request, match_id=match.id)
        assert action.common.get('match').id == match.id


class TestGetMatchByIdActionRun:

    def test_it_returns_match(self):
        action = GetMatchByIdAction()
        match = MatchFactory.build()
        request = get_fake_request()
        action.common = {'match': match}
        result = json.loads(action.run(request, match_id=match.id).content)
        expected = {
            'match': {
                'id': match.id,
                'sets_number': match.sets_number,
                'access_code': match.access_code,
                'status': match.status,
                'game_status': match.game_status,
                'set_points_number': match.set_points_number,
                'points_difference': match.points_difference,
                'tie_break_points': match.tie_break_points,
                'teams': [],
                'sets': [],
                'winner_team': match.winner_team,
            }
        }
        assert expected == result
