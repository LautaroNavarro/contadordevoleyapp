import pytest
from match.tests.factories.match_factory import MatchFactory
from match.models.match import Match
from match.models.set import Set
from match.tests.factories.team_factory import TeamFactory
from match.tests.factories.set_factory import (
    SetFinishedTeamOneFactory,
    SetFinishedTeamTwoFactory,
    SetFactory,
)

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

    @pytest.mark.django_db
    def test_team_one_is_team_one(self):
        match = MatchFactory(sets_number=7)
        teams = [TeamFactory() for i in range(2)]
        match.teams.add(*teams)
        assert match.team_one.id == teams[0].id

    @pytest.mark.django_db
    def test_team_two_is_team_two(self):
        match = MatchFactory(sets_number=7)
        teams = [TeamFactory() for i in range(2)]
        match.teams.add(*teams)
        assert match.team_two.id == teams[1].id

    @pytest.mark.django_db
    def test_get_counters(self):
        match = MatchFactory(sets_number=7)
        SetFinishedTeamOneFactory(match=match)
        t1c, t2c = match.get_counters()
        assert t1c == 1
        assert t2c == 0
        SetFinishedTeamOneFactory(match=match)
        t1c, t2c = match.get_counters()
        assert t1c == 2
        assert t2c == 0
        SetFinishedTeamTwoFactory(match=match)
        t1c, t2c = match.get_counters()
        assert t1c == 2
        assert t2c == 1
        SetFinishedTeamTwoFactory(match=match)
        t1c, t2c = match.get_counters()
        assert t1c == 2
        assert t2c == 2

    @pytest.mark.django_db
    def test_winner_team_no_winner(self):
        match = MatchFactory(sets_number=3)
        teams = [TeamFactory() for i in range(2)]
        match.teams.add(*teams)
        SetFinishedTeamOneFactory(match=match)
        assert match.winner_team is None

    @pytest.mark.django_db
    def test_winner_team_returns_team_one(self):
        match = MatchFactory(sets_number=3)
        teams = [TeamFactory() for i in range(2)]
        match.teams.add(*teams)
        SetFinishedTeamOneFactory(match=match)
        SetFinishedTeamOneFactory(match=match)
        assert match.winner_team.id == teams[0].id

    @pytest.mark.django_db
    def test_winner_team_returns_team_two(self):
        match = MatchFactory(sets_number=3)
        teams = [TeamFactory() for i in range(2)]
        match.teams.add(*teams)
        SetFinishedTeamTwoFactory(match=match)
        SetFinishedTeamTwoFactory(match=match)
        assert match.winner_team.id == teams[1].id

    @pytest.mark.django_db
    def test_new_set_should_be_tie_break_false(self):
        match = MatchFactory(sets_number=5)
        teams = [TeamFactory() for i in range(2)]
        match.teams.add(*teams)
        SetFinishedTeamTwoFactory(match=match)
        SetFinishedTeamTwoFactory(match=match)
        assert match.new_set_should_be_tie_break() is False

    @pytest.mark.django_db
    def test_new_set_should_be_tie_break_true(self):
        match = MatchFactory(sets_number=5)
        teams = [TeamFactory() for i in range(2)]
        match.teams.add(*teams)
        SetFinishedTeamTwoFactory(match=match)
        SetFinishedTeamTwoFactory(match=match)
        SetFinishedTeamOneFactory(match=match)
        SetFinishedTeamOneFactory(match=match)
        assert match.new_set_should_be_tie_break() is True

    @pytest.mark.django_db
    def test_update_game_status_case_one(self):
        """
        Case one description:
            Match
                sets to play 3
                sets played 2
                points 25
                game_status: Playing
                sets [
                    {
                        game_status: Finished
                        t1: 25
                        t2: 0
                    }
                    {
                        game_status: Playing
                        t1: 25
                        t2: 0
                    }
                ]
        change SET game_status to Finished
        change MATCH game_status to Finished
        """
        match = MatchFactory(sets_number=3)
        teams = [TeamFactory() for i in range(2)]
        match.teams.add(*teams)
        SetFinishedTeamOneFactory(match=match)
        _set = SetFinishedTeamOneFactory(match=match)
        match.update_game_status()
        assert Set.objects.get(id=_set.id).game_status == Set.GameStatus.FINISHED.value
        assert match.game_status == Match.GameStatus.FINISHED.value
        assert Set.objects.filter(match=match).count() == 2

    @pytest.mark.django_db
    def test_update_game_status_case_two(self):
        """
        Case two description:
            Match
                sets to play 5
                sets played 2
                points 25
                game_status: Playing
                sets [
                    {
                        game_status: Finished
                        t1: 25
                        t2: 0
                    }
                    {
                        game_status: Playing
                        t1: 25
                        t2: 0
                    }
                ]
        change SET game status to FINISHED
        MATCH game status should be PLAYING
        new SET SHOULD BE CREATED
        """
        match = MatchFactory(sets_number=5)
        teams = [TeamFactory() for i in range(2)]
        match.teams.add(*teams)
        SetFinishedTeamOneFactory(match=match)
        _set = SetFactory(match=match, team_one_points=25)
        match.update_game_status()
        assert Set.objects.get(id=_set.id).game_status == Set.GameStatus.FINISHED.value
        assert match.game_status == Match.GameStatus.PLAYING.value
        assert Set.objects.filter(match=match).count() == 3
        new_set = Set.objects.filter(match=match).order_by('id').last()
        assert new_set.game_status == Set.GameStatus.PLAYING.value
        assert new_set.team_one_points == 0
        assert new_set.team_two_points == 0
        assert new_set.is_tie_break is False
        assert new_set.set_number == 3

    @pytest.mark.django_db
    def test_update_game_status_case_three(self):
        """
        Case three description:
            Match
                sets to play 5
                sets played 4
                points 25
                game_status: Playing
                sets [
                    {
                        game_status: Finished
                        t1: 25
                        t2: 0
                    }
                    {
                        game_status: Playing
                        t1: 25
                        t2: 0
                    }
                    {
                        game_status: Finished
                        t1: 0
                        t2: 25
                    }
                    {
                        game_status: Finished
                        t1: 0
                        t2: 25
                    }
                ]
        change SET game status to FINISHED
        MATCH game status should be PLAYING
        new SET SHOULD BE CREATED
        """
        match = MatchFactory(sets_number=5)
        teams = [TeamFactory() for i in range(2)]
        match.teams.add(*teams)
        SetFinishedTeamOneFactory(match=match)
        SetFinishedTeamOneFactory(match=match)
        SetFinishedTeamTwoFactory(match=match)
        _set = SetFactory(match=match, team_two_points=25)
        match.update_game_status()
        assert Set.objects.get(id=_set.id).game_status == Set.GameStatus.FINISHED.value
        assert match.game_status == Match.GameStatus.PLAYING.value
        assert Set.objects.filter(match=match).count() == 5
        new_set = Set.objects.filter(match=match).order_by('id').last()
        assert new_set.game_status == Set.GameStatus.PLAYING.value
        assert new_set.team_one_points == 0
        assert new_set.team_two_points == 0
        assert new_set.is_tie_break is True
        assert new_set.set_number == 5

    @pytest.mark.django_db
    def test_update_game_status_case_four(self):
        """
        Case four description:
            Match
                sets to play 5
                sets played 5
                points 25
                game_status: Playing
                sets [
                    {
                        game_status: Finished
                        t1: 25
                        t2: 0
                    }
                    {
                        game_status: Playing
                        t1: 25
                        t2: 0
                    }
                    {
                        game_status: Finished
                        t1: 0
                        t2: 25
                    }
                    {
                        game_status: Finished
                        t1: 0
                        t2: 25
                    }
                    {
                        game_status: Finished
                        t1: 0
                        t2: 15
                    }
                ]
        change SET game status to FINISHED
        MATCH game status should be FINISHED
        """
        match = MatchFactory(sets_number=5)
        teams = [TeamFactory() for i in range(2)]
        match.teams.add(*teams)
        SetFinishedTeamOneFactory(match=match)
        SetFinishedTeamOneFactory(match=match)
        SetFinishedTeamTwoFactory(match=match)
        SetFinishedTeamTwoFactory(match=match)
        _set = SetFactory(match=match, team_two_points=15, is_tie_break=True)
        match.update_game_status()
        assert Set.objects.get(id=_set.id).game_status == Set.GameStatus.FINISHED.value
        assert match.game_status == Match.GameStatus.FINISHED.value
        assert Set.objects.filter(match=match).count() == 5

    @pytest.mark.django_db
    def test_can_substract_points_no_points_playing_set_returns_false(self):
        match = MatchFactory(sets_number=5)
        SetFactory(match=match)
        assert match.can_substract_points('team_one') is False

    @pytest.mark.django_db
    def test_can_substract_points_no_set_returns_false(self):
        match = MatchFactory(sets_number=5)
        assert match.can_substract_points('team_one') is False

    @pytest.mark.django_db
    def test_can_substract_points_finished_sets_returns_false(self):
        match = MatchFactory(sets_number=5)
        SetFactory(match=match, game_status=Set.GameStatus.FINISHED.value)
        assert match.can_substract_points('team_one') is False

    @pytest.mark.django_db
    def test_can_substract_points_playing_set_return_true(self):
        match = MatchFactory(sets_number=5)
        SetFactory(match=match, game_status=Set.GameStatus.PLAYING.value, team_one_points=1)
        assert match.can_substract_points('team_one') is True

    @pytest.mark.django_db
    def test_can_substract_points_playing_set_return_false_team_two(self):
        match = MatchFactory(sets_number=5)
        SetFactory(match=match, game_status=Set.GameStatus.PLAYING.value, team_one_points=1)
        assert match.can_substract_points('team_two') is False

    @pytest.mark.django_db
    def test_get_team_one_and_team_two_won_sets_returns_one_and_cero(self):
        match = MatchFactory(sets_number=5)
        SetFinishedTeamOneFactory(match=match)
        team_one, team_two = match.get_team_one_and_team_two_won_sets(match.set_set.all())
        assert team_one == 1
        assert team_two == 0

    @pytest.mark.django_db
    def test_get_team_one_and_team_two_won_sets_returns_two_and_cero(self):
        match = MatchFactory(sets_number=5)
        SetFinishedTeamOneFactory(match=match)
        SetFinishedTeamOneFactory(match=match)
        team_one, team_two = match.get_team_one_and_team_two_won_sets(match.set_set.all())
        assert team_one == 2
        assert team_two == 0

    @pytest.mark.django_db
    def test_get_team_one_and_team_two_won_sets_returns_one_and_one(self):
        match = MatchFactory(sets_number=5)
        SetFinishedTeamOneFactory(match=match)
        SetFinishedTeamTwoFactory(match=match)
        team_one, team_two = match.get_team_one_and_team_two_won_sets(match.set_set.all())
        assert team_one == 1
        assert team_two == 1

    @pytest.mark.django_db
    def test_get_team_one_and_team_two_won_sets_returns_cero_and_cero(self):
        match = MatchFactory(sets_number=5)
        team_one, team_two = match.get_team_one_and_team_two_won_sets(match.set_set.all())
        assert team_one == 0
        assert team_two == 0
