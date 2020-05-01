import pytest
from httperrors import BadRequestError
from match.helpers.testing_helpers import get_fake_request
from match.views.base.base_paginated_action import PaginatedBaseAction
from match.constants.error_codes import INVALID_PAGE


class TestBasePaginatedAction:

    def test_some(self):
        action = PaginatedBaseAction()
        request = get_fake_request(get_params={'page': 0})
        with pytest.raises(BadRequestError) as e:
            action.validate(request)
            assert e.error_message == 'Page number must be positive'
            assert e.error_code == INVALID_PAGE
