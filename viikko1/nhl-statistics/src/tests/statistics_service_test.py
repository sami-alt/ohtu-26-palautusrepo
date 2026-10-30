import unittest

from player import Player
from statistics_service import SortBy, StatisticsService


class StubPlayerReader:
    def __init__(self, players):
        self._players = players

    def get_players(self):
        return self._players


class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        players = [
            Player("Aarne Ahma", "HIF", 10, 1),
            Player("Bertta Bear", "TPS", 8, 10),
            Player("Cecilia Cat", "HIF", 12, 2),
        ]
        self.service = StatisticsService(StubPlayerReader(players))

    def test_search_finds_player(self):
        player = self.service.search("Bertta")

        self.assertEqual(player.name, "Bertta Bear")

    def test_search_returns_none_when_player_is_not_found(self):
        player = self.service.search("Unknown")

        self.assertIsNone(player)

    def test_team_returns_players_from_the_requested_team(self):
        players = self.service.team("HIF")

        self.assertEqual([player.name for player in players], ["Aarne Ahma", "Cecilia Cat"])

    def test_top_returns_players_in_points_order(self):
        players = self.service.top(2)

        self.assertEqual(
            [player.name for player in players],
            ["Bertta Bear", "Cecilia Cat"]
        )

    def test_top_can_sort_players_by_goals(self):
        players = self.service.top(2, SortBy.GOALS)

        self.assertEqual(
            [player.name for player in players],
            ["Cecilia Cat", "Aarne Ahma"]
        )

    def test_top_can_sort_players_by_assists(self):
        players = self.service.top(2, SortBy.ASSISTS)

        self.assertEqual(
            [player.name for player in players],
            ["Bertta Bear", "Cecilia Cat"]
        )
