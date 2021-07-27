from pydoc import describe
from discord import Embed, Color


def create_team_emded(time: int, game: str):
    embed = Embed(colour=Color.dark_gold(
    ), description=f"Time to play {game.content},react with  👍 if u in", title="Matchmaking")
    embed.set_footer(text=f"Ends in {str(time)} seconds")

    return embed
