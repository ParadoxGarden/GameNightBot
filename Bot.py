import json

import discord

import TTS
import Voting


class MyClient(discord.Client):
    voice_engine = TTS.init_voice()
    voice_client = None
    bot_variables = None
    prefix = None
    vote_emojis = list()
    vote = Voting.Voting()

    def initVars(self, filename):
        settings = open(filename, "r")
        self.bot_variables = json.loads(settings.read())
        settings.close()

    async def on_ready(self):
        self.prefix = self.bot_variables["Prefix"]

        emoji_names = self.bot_variables["VoteEmojis"]

        voice_engine_voices = self.voice_engine.getProperty("voices")
        self.voice_engine.setProperty('rate', int(self.bot_variables['TTS']['Rate']))
        self.voice_engine.setProperty('volume', float(self.bot_variables['TTS']['Volume']))
        self.voice_engine.setProperty('voice', voice_engine_voices[int(self.bot_variables['TTS']['Voice'])])

        for emoji in self.emojis:
            if emoji.name in emoji_names:
                self.vote_emojis.append(emoji)

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
        content = message.content
        channel = message.channel
        guild = message.guild
        voice_channels = guild.voice_channels

        # we do not want the bot to reply to itself
        if author.bot:
            return

        # check for banned words being used
        if self.bot_variables["Censoring"] == 1:
            for word in self.bot_variables["BannedWords"]:
                if word.lower() in content.lower():
                    await message.delete()
                    await channel.send("Boop!", delete_after=5)
                    await author.send(
                        "Sorry friend, you used a banned word, the message you sent was deleted. " +
                        " if you feel this was done in error, please contact an administrator")
                    await author.send(
                        "the message that contained the word was: \"" + content + "\", the word was \"" + word + "\"")
                    return

        # check for actual commands being used
        if message.content[:len(self.prefix)] == self.prefix:
            real_content = message.content[len(self.prefix):].lower().strip().split(" ")

            if real_content[0] == 'help':
                await message.delete()

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

            elif real_content[0] == "react":
                message_sent = await channel.send("Testing shit")
                for emoji in self.vote_emojis:
                    await message_sent.add_reaction(emoji)
                await message_sent.add_reaction("🚫")
                print("Testing reactions")

            elif real_content[0] == "dev":
                for emoji in self.vote_emojis:
                    print(emoji.name)

            elif real_content[0] == "join":
                await self.join_func(author, voice_channels)

            elif real_content[0] in ["quit", "fuckoff", "leave", "kys", "end"]:
                if self.voice_client is not None:
                    await self.voice_client.disconnect()
                self.voice_client = None
                print("Leaving voice channel")

            elif real_content[0] == "tts":
                text = ' '.join(real_content[1:])
                if self.voice_client is not None:
                    self.tts_play(text)
                else:
                    await self.join_func(author, voice_channels)
                    self.tts_play(text)
                print("Playing tts message: " + text)

    async def tts_play(self, text):
        self.voice_engine.save_to_file(text, "temp.mp3")
        self.voice_engine.runAndWait()
        player = discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source="temp.mp3")
        self.voice_client.play(player)

    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return
        else:
            if reaction.emoji == "🚫":
                message = reaction.message
                for react in message.reactions:
                    await react.remove(user)
            else:
                return
    async def on_reaction_remove(self, reaction, user):
        #  if reaction.author.user.id
        if user.bot:
            return
        else:
            return


def run_bot():
    client = MyClient()
    client.initVars("settings.json")
    client.run(client.bot_variables["Token"])

if __name__ == "__main__":
    run_bot()
