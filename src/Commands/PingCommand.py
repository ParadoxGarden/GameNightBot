import Command

class PingCommand(Command):
    msg = None
    register = [
        "Ping"
    ]
    def __init__(self, msg) -> None:
        self.msg = msg
    async def execute(self, bot):
        await self.msg.channel.send("pong")
def makeCommand(msg):
    return PingCommand(msg)
