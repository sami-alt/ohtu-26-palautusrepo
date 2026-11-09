import argparse

from rich.console import Console
from rich.table import Table

from player_reader import PlayerReader
from player_stats import PlayerStats


def parse_args():
    parser = argparse.ArgumentParser(
        description="List NHL players ranked by points."
    )
    parser.add_argument(
        "-n",
        "--nationality",
        default="FIN",
        help="Three-letter nationality code (default: FIN)",
    )
    parser.add_argument(
        "-l",
        "--limit",
        type=int,
        default=0,
        help="Show only the first N players (default: all)",
    )
    args = parser.parse_args()

    if args.limit < 0:
        parser.error("--limit must be a non-negative integer")
    return args


def get_top_players(args):
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    players = PlayerReader(url).get_players()
    top_players = PlayerStats(players).top_scorers_by_nationality(
        args.nationality.upper()
    )
    if args.limit:
        top_players = top_players[:args.limit]
    return top_players


def create_table(nationality):
    table = Table(
        title=f"Top NHL scorers from {nationality.upper()}",
        title_style="bold cyan",
        show_lines=False,
    )
    table.add_column("#", justify="right", style="dim")
    table.add_column("Player", style="bold")
    table.add_column("Team")
    table.add_column("Games", justify="right")
    table.add_column("Goals", justify="right")
    table.add_column("Assists", justify="right")
    table.add_column("Points", justify="right", style="bold green")
    return table


def add_players_to_table(table, players):
    for rank, player in enumerate(players, start=1):
        points = player.goals + player.assists
        table.add_row(
            str(rank),
            player.name,
            player.team,
            str(player.games),
            str(player.goals),
            str(player.assists),
            str(points),
        )


def main():
    args = parse_args()
    top_players = get_top_players(args)
    table = create_table(args.nationality)
    add_players_to_table(table, top_players)
    Console().print(table)


if __name__ == "__main__":
    main()
