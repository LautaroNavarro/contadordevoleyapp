import pytest
from httperrors import BadRequestError
from match.helpers.testing_helpers import get_fake_jwt_request
from match.views.base.base_paginated_view import PaginatedBaseView
from match.constants.error_codes import INVALID_PAGE


class TestBasePaginatedView:

    def test_some(self):
        view = PaginatedBaseView()
        request = get_fake_jwt_request(get_params={'page': 0})
        with pytest.raises(BadRequestError) as e:
            view.validate(request)
            assert e.error_message == 'Page number must be positive'
            assert e.error_code == INVALID_PAGE
