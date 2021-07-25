import Command

class ClearCommand(Command):
    msg = None
    register = [
        "Clear",
        "Remove"
    ]
    def __init__(self, msg) -> None:
        self.msg = msg
    async def execute(self, bot):
        channel = self.msg.channel
        real_content = self.msg.content[len(self.prefix):].lower().strip().split(" ")
        await self.msg.delete()
        if len(real_content) > 1:
            messages = await channel.history(limit=int(real_content[1])).flatten()
            await channel.delete_messages(messages)
            print("Clearing" + real_content[1] + "messages")
        else:
            messages = await channel.history(limit=10).flatten()
            await channel.delete_messages(messages)
            print("Clearing 10 messages")
def makeCommand(msg):
    return ClearCommand(msg)
