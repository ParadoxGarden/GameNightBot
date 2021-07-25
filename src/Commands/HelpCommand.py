import Command

class HelpCommand(Command):
    msg = None
    register = [
        "Help",
        "?"
    ]
    def __init__(self, msg) -> None:
        self.msg = msg
    async def execute(self, bot):
        await self.msg.delete()
def makeCommand(msg):
    return HelpCommand(msg)
