import discord

import TTS

bot_variables = dict()
banned_words = list()

reaction_user_data = dict()
reaction_number_data = dict()

voice_engine = TTS.init_voice()
voice_client = None

config_message = None
editing_message = None

display_emojis = list()


def import_settings():
    settings = open("settings.txt", "r")
    banned = open("bannedwords.txt", "r")
    global banned_words
    global bot_variables

    # Defining settings file structure
    for line in settings:
        line = line.strip()
        # Comment
        if "#" == line[:1]:
            pass
        # New Line
        elif "" == line:
            pass
        # Anything else
        else:
            linelist = line.split("=")
            bot_variables[linelist[0].lower()] = linelist[1]

    # Defining each banned word
    for word in banned:
        word = word.strip()
        # Comment
        if "#" == word[:1]:
            pass
        # New Line
        elif "" == word:
            pass
        else:
            banned_words.append(word)
    voice_engine.setProperty('rate', int(bot_variables.get('rate')))
    voice_engine.setProperty('volume', float(bot_variables.get('volume')))
    voice_engine.setProperty('voice', voice_engine.getProperty("voices")[int(bot_variables.get("voice"))])
    settings.close()
    banned.close()


class MyClient(discord.Client):
    global banned_words
    global bot_variables

    async def on_ready(self):
        print('------')
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def join_func(self, author, channels):
        global voice_client
        for channel in channels:
            if author in channel.members:
                voice_client = await channel.connect()
        print("Joining a channel")

    async def on_message(self, message):
        global voice_client
        global reaction_user_data
        global reaction_number_data
        global config_message
        author = message.author
        content = message.content
        channel = message.channel
        guild = message.guild
        emoji_list = guild.emojis
        voice_channels = guild.voice_channels
        prefix = bot_variables.get("prefix")

        # we do not want the bot to reply to itself
        if author.bot:
            return
        # check for banned words being used
        if bot_variables.get("censoring") == 1:
            for word in banned_words:
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
        if message.content[:len(prefix)] == prefix:
            real_content = message.content[len(prefix):].lower().strip().split(" ")

            if real_content[0] == 'help':
                await message.delete()
                message = await channel.send("do not step")
                for emoji in guild.emojis:
                    if emoji.name == "donot":
                        await message.add_reaction(emoji)
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

            elif real_content[0] == "reset":
                reaction_user_data = dict()
                reaction_number_data = dict()
                print("Resetting reaction data structures")

            elif real_content[0] == "react":
                if display_emojis is not None:
                    message_sent = await channel.send("Testing shit")
                    for emoji in display_emojis:
                        await message_sent.add_reaction(emoji)
                    print("Testing reactions")
                else:
                    print("Configure First")

            elif real_content[0] == "dev":
                for emoji in display_emojis:
                    print(emoji.name)
                for key in reaction_user_data.keys():
                    print("\n")
                    for sub_list in reaction_user_data[key]:
                        print(sub_list)

            elif real_content[0] == "join":
                await self.join_func(author, voice_channels)

            elif real_content[0] == "config":
                if config_message is None:
                    message_sent = await channel.send("Testing shit")
                    for emoji in emoji_list:
                        await message_sent.add_reaction(emoji)
                    print("Testing reactions")
                    config_message = message_sent
                else:
                    print("already configured")

            elif real_content[0] in ["quit", "fuckoff", "kys", "end"]:
                if voice_client is not None:
                    await voice_client.disconnect()
                voice_client = None
                print("Leaving voice channel")

            elif real_content[0] == "tts":
                text = ' '.join(real_content[1:])
                voice_engine.save_to_file(text, "temp.mp3")
                voice_engine.runAndWait()
                if voice_client is not None:
                    player = discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source="temp.mp3")
                    voice_client.play(player)
                else:
                    await self.join_func(author, voice_channels)
                    player = discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source="temp.mp3")
                    voice_client.play(player)
                print("Playing tts message: " + text)

    async def on_reaction_add(self, reaction, user):
        if reaction.message == config_message:
            display_emojis.append(reaction.emoji)
            print(display_emojis)
            return
        if user.bot:
            return
        else:
            if user in reaction_user_data.keys():
                react_list = reaction_user_data.get(user)
                if len(react_list) == 3:
                    await reaction.remove(user)
                else:
                    react_list.append([len(react_list) + 1, reaction.emoji])
            else:
                reaction_user_data[user] = [[1, reaction.emoji]]
            return

    async def on_reaction_remove(self, reaction, user):
        #  if reaction.author.user.id
        if user.bot:
            return
        else:
            if user in reaction_user_data.keys():
                react_list = reaction_user_data.get(user)
                for sub_list in react_list:
                    if reaction.emoji in sub_list:
                        stated_list = sub_list
                if stated_list[0] == 1:
                    for sub_list in react_list:
                        sub_list[0] = sub_list[0] - 1
                    react_list.remove(stated_list)
                elif stated_list[0] == 2:
                    react_list[2][0] = 2
                    react_list.remove(stated_list)
                elif stated_list[0] == 3:
                    react_list.remove(stated_list)
            return


def run_bot():
    client = MyClient()
    client.run(bot_variables.get("token"))


def init():
    import_settings()
    run_bot()


if __name__ == "__main__":
    init()
