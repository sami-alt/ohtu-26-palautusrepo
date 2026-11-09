import unittest

from player import Player
from player_stats import PlayerStats


def create_player(name, team, goals, assists):
    return Player({
        "name": name,
        "nationality": "FIN",
        "assists": assists,
        "goals": goals,
        "team": team,
        "games": 1,
        "id": name,
    })


class TestPlayerStats(unittest.TestCase):
    def setUp(self):
        self.players = [
            create_player("A", "NHL", 10, 20),
            create_player("B", "NHL", 15, 5),
            create_player("C", "SHL", 30, 30),
        ]
        self.stats = PlayerStats(self.players)

    def test_top_scorers_by_nationality(self):
        result = self.stats.top_scorers_by_nationality("FIN")

        self.assertEqual([player.name for player in result], ["C", "A", "B"])

    def test_top_goal_scorers_returns_requested_number(self):
        result = self.stats.top_goal_scorers(2)

        self.assertEqual([player.name for player in result], ["C", "B"])

    def test_top_scorers_by_team(self):
        result = self.stats.top_scorers_by_team("NHL")

        self.assertEqual([player.name for player in result], ["A", "B"])

    def test_top_scorers_by_team_returns_empty_for_unknown_team(self):
        result = self.stats.top_scorers_by_team("UNKNOWN")

        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
