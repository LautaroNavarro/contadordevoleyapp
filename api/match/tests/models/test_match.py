from match.tests.factories.match_factory import MatchFactory


class TestGameLogic:

    def test_get_minimum_sets_to_play_return_3_when_sets_is_5(self):
        match = MatchFactory.build(sets_number=5)
        result = match.get_minimum_sets_to_play()
        assert result == 3

    def test_get_minimum_sets_to_play_return_2_when_sets_is_3(self):
        match = MatchFactory.build(sets_number=3)
        result = match.get_minimum_sets_to_play()
        assert result == 2

    def test_get_minimum_sets_to_play_return_1_when_sets_is_1(self):
        match = MatchFactory.build(sets_number=1)
        result = match.get_minimum_sets_to_play()
        assert result == 1

    def test_get_minimum_sets_to_play_return_4_when_sets_is_7(self):
        match = MatchFactory.build(sets_number=7)
        result = match.get_minimum_sets_to_play()
        assert result == 4
