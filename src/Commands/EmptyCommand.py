import Command

class EmptyCommand(Command):
    msg = None
    def __init__(self, msg) -> None:
        self.msg = msg
    async def execute(self, bot):
        await self.msg.channel.send("No command with that register foundfound")
def makeCommand(msg):
    return EmptyCommand(msg)
