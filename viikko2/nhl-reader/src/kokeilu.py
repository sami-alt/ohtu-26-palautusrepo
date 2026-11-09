from player import Player
from player_stats import PlayerStats


def main():
    players = [
        Player({
            "name": "Aleksi Example",
            "nationality": "FIN",
            "assists": 20,
            "goals": 15,
            "team": "NHL",
            "games": 40,
            "id": 1,
        }),
        Player({
            "name": "Toinen Example",
            "nationality": "FIN",
            "assists": 10,
            "goals": 18,
            "team": "NHL",
            "games": 40,
            "id": 2,
        }),
        Player({
            "name": "Kolmas Example",
            "nationality": "SWE",
            "assists": 30,
            "goals": 5,
            "team": "SHL",
            "games": 40,
            "id": 3,
        }),
    ]

    team_players = PlayerStats(players).top_scorers_by_team("NHL")
    for player in team_players:
        points = player.goals + player.assists
        print(f"{player.name}: {points} points")


if __name__ == "__main__":
    main()
