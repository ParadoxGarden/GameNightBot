import json
import discord
import TTS


class Game():
    def __init__(self, name, emoji, special=None):
        self.name = name
        self.emoji = emoji

class Vote():
    def __init__(self, emoji, count, game):
        self.emoji = emoji
        self.count = count
        self.game = game


class MyClient(discord.Client):
    async def on_ready(self):

        # INIT
        self.guild = None
        self.vmessage = None
        settings = open("settings.json", "r")
        self.bot_variables = json.loads(settings.read())
        self.voice_engine = TTS.init_voice()
        self.prefix = self.bot_variables["Prefix"]
        settings.close()
        for guild in self.guilds:
            if guild.name == "Game Night":
                self.guild = guild
        

        for channel in self.guild.channels:
            if channel.name == "voting":
                self.vchannel = channel
            elif channel.name == "announcements":
                self.achannel = channel
            elif channel.name == "intra-bot-communication":
                self.ichannel = channel

        # games we can play
        self.games_list = list()
        for game in self.bot_variables.get("Games"):
            self.games_list.append(Game(game.get("Name"), game.get("Emoji")))
        # emojis they use
        self.vote_emojis = list()
        name_list = list()
        for game in self.games_list:
            name_list.append(game.emoji)
        for emoji in guild.emojis:
            if emoji.name in name_list:
                self.vote_emojis.append(emoji)

        # init voice engine
        voice_engine_voices = self.voice_engine.getProperty("voices")
        self.voice_engine.setProperty(
            'rate', int(self.bot_variables['TTS']['Rate']))
        self.voice_engine.setProperty('volume', float(
            self.bot_variables['TTS']['Volume']))
        self.voice_engine.setProperty(
            'voice', voice_engine_voices[int(self.bot_variables['TTS']['Voice'])])
        self.voice_client = guild.voice_client

        # ensure the user knows we're running
        print('------')
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def join_func(self, author, channels):
        for channel in channels:
            if author in channel.members:
                self.voice_client = await channel.connect()
        print("Joining a channel")

    async def on_message(self, message):
        author = message.author

        # we do not want the bot to reply to itself
        if author.bot:
            if message.channel is self.ichannel:
                method = getattr(self, message.content.strip())
                await method()
            else:
                pass

        content = message.content
        channel = message.channel

        # check for banned words being used
        if int(self.bot_variables["Censoring"]) == 1:
            for word in self.bot_variables["BannedWords"]:
                if word.lower() in content.lower():
                    await message.delete()
                    await channel.send("Bloop!", delete_after=5)
                    await author.send(
                        "Sorry friend, you used a banned word, the message you sent was deleted. " +
                        " if you feel this was done in error, please contact an administrator")
                    await author.send(
                        "the message that contained the word was: \"" + content + "\", the word was \"" + word + "\"")
                    return

        guild = message.guild
        voice_channels = guild.voice_channels

        # check for actual commands being used
        if message.content[:len(self.prefix)] == self.prefix:
            real_content = message.content[len(
                self.prefix):].lower().strip().split(" ")
            if real_content[0] == 'help':
                await message.delete()

            elif real_content[0] == 'ping':
                await message.channel.send("pong")

            elif real_content[0] == 'clear':
                await message.delete()
                if len(real_content) > 1:
                    messages = await channel.history(limit=int(real_content[1])).flatten()
                    await channel.delete_messages(messages)
                    print("Clearing" + real_content[1] + "messages")
                else:
                    messages = await channel.history(limit=10).flatten()
                    await channel.delete_messages(messages)
                    print("Clearing 10 messages")

            elif real_content[0] == "dev":
                await self.begin_voting_period()

            elif real_content[0] == "join":
                await self.join_func(author, voice_channels)

            elif real_content[0] in ["quit", "fuck off" "fuckoff", "leave", "kys", "end"]:
                if self.voice_client is not None:
                    await self.voice_client.disconnect()
                self.voice_client = None
                print("Leaving voice channel")

            elif real_content[0] == "tts":
                text = ' '.join(real_content[1:])
                if self.voice_client is not None:
                    await self.tts_play(text)
                else:
                    await self.join_func(author, voice_channels)
                    await self.tts_play(text)
                print("Playing tts message: " + text)

    async def tts_play(self, text):
        self.voice_engine.save_to_file(text, "temp.mp3")
        self.voice_engine.runAndWait()
        player = discord.FFmpegPCMAudio(source="temp.mp3")
        self.voice_client.play(player)

    async def collate_votes(self):
        vmessage = await self.vchannel.fetch_message(self.vchannel.last_message_id)
        votes = list()
        for react in vmessage.reactions:
            for game in self.games_list:
                if game.emoji == react.emoji.name:
                    votes.append(Vote(react.emoji, react.count, game))
        
        print("Votes Collected")

        return [votes]

    async def begin_voting_period(self): 
        self.vmessage = await self.vchannel.send("```Vote for what game you want to play next Monday by clicking on the emoji under this message!```")
        for emoji in self.vote_emojis:
            await self.vmessage.add_reaction(emoji)
        
        print("Voting period started")

    async def begin_game_night(self):
        votes = self.collate_votes()

        top = Vote(None, 0, None)
        for vote in votes:
            if top.count < vote.count:
                top = vote
        print(top.game.name + " won the vote!")
        print("With " + top.count + " votes!")
        self.achannel.send(top.game.name + " won the vote!\n" + "With " + top.count + " votes!")
        


def run_bot():
    client = MyClient()
    settings = open("settings.json", "r")
    key = json.loads(settings.read())
    settings.close()
    client.run(key["Token"])


if __name__ == "__main__":
    run_bot()
