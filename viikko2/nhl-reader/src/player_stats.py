# pylint: disable=too-few-public-methods
class PlayerStats:
    def __init__(self, players):
        self.players = players

    def top_scorers_by_nationality(self, nationality):
        players = [
            player for player in self.players
            if player.nationality == nationality
        ]
        return sorted(
            players,
            key=lambda player: player.goals + player.assists,
            reverse=True,
        )

    def top_goal_scorers(self, how_many):
        """Palauttaa eniten maaleja tehneet pelaajat."""
        return sorted(
            self.players,
            key=lambda player: player.goals,
            reverse=True,
        )[:how_many]

    def top_scorers_by_team(self, team):
        """Palauttaa joukkueen pelaajat pisteiden mukaan laskevassa järjestyksessä."""
        team_players = [
            player for player in self.players
            if player.team == team
        ]
        return sorted(
            team_players,
            key=lambda player: player.goals + player.assists,
            reverse=True,
        )
