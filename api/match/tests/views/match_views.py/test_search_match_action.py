import pytest
import json
from httperrors import (
    NotFoundError,
    BadRequestError,
)
from match.views.match_actions.search_match_action import SearchMatchAction
from match.helpers.testing_helpers import get_fake_request
from match.constants.error_codes import (
    INVALID_ACCESS_CODE,
    REQUIRED_QUERY_PARAM,
)
from match.tests.factories.match_factory import MatchFactory
from match.models.match import Match


@pytest.mark.django_db
class TestSearchMatchActionValidate:

    def test_it_raises_not_found_when_invalid_access_code(self):
        action = SearchMatchAction()
        request = get_fake_request(get_params={'access_code': '123AS'})
        with pytest.raises(NotFoundError) as e:
            action.validate(request)
        assert e.value.error_code == INVALID_ACCESS_CODE

    def test_it_raises_bad_request_when_access_code_not_provided(self):
        action = SearchMatchAction()
        request = get_fake_request()
        with pytest.raises(BadRequestError) as e:
            action.validate(request)
        assert e.value.error_code == REQUIRED_QUERY_PARAM

    def test_it_raises_not_found_when_match_is_not_live(self):
        action = SearchMatchAction()
        match = MatchFactory(status=Match.Status.ARCHIVED.value)
        request = get_fake_request(get_params={'access_code': match.access_code})
        with pytest.raises(NotFoundError) as e:
            action.validate(request, match_id=match.id)
        assert e.value.error_code == INVALID_ACCESS_CODE

    def test_it_does_not_raise_error_when_valid_id_and_write_match_in_common(self):
        action = SearchMatchAction()
        match = MatchFactory()
        request = get_fake_request(get_params={'access_code': match.access_code})
        action.validate(request, match_id=match.id)
        assert action.common.get('match').id == match.id


class TestSearchMatchActionRun:

    def test_it_returns_match(self):
        action = SearchMatchAction()
        match = MatchFactory.build()
        request = get_fake_request()
        action.common = {'match': match}
        result = json.loads(action.run(request).content)
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
