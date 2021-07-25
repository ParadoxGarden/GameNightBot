import Command

class GamesCommand(Command):
    msg = None
    register = [
        "Game",
        "Games"
    ]
    def __init__(self, msg) -> None:
        self.msg = msg
    async def execute(self, bot):
        msg = "\nGames List\n"
        for item in bot.games_list:
            msg = msg + f"{item.name} : {item.real_emoji}\n"
        msg = msg + ""
        await self.msg.channel.send(msg)
def makeCommand(msg):
    return GamesCommand(msg)
