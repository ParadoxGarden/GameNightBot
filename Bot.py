import discord

botVars = dict()
bannedWords = list()
reactionData = dict()


def import_settings():
    settings = open("settings.txt", "r")
    banned = open("bannedwords.txt", "r")
    global bannedWords
    global botVars

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
            botVars[linelist[0].lower()] = linelist[1]

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
            bannedWords.append(word)

    settings.close()
    banned.close()


class MyClient(discord.Client):
    global bannedWords
    global botVars

    async def on_ready(self):
        print('------')
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        author = message.author
        content = message.content
        channel = message.channel
        guild = message.guild
        emoji_list = guild.emojis

        prefix = botVars.get("prefix")

        # we do not want the bot to reply to itself
        if author.id == self.user.id:
            return
        # check for banned words being used
        for word in bannedWords:
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
            realContent = message.content[len(prefix):].lower().strip().split(" ")
            if realContent[0] == 'help':
                await message.delete()
                await channel.send()
            elif realContent[0] == 'clear':
                await message.delete()
                messages = await channel.history(limit=int(realContent[1])).flatten()
                await channel.delete_messages(messages)
            elif realContent[0] == "react":
                messageSent = await channel.send("Testing shit")
                for emoji in emoji_list:
                    await messageSent.add_reaction(emoji)

    async def on_reaction_add(self, reaction, user):
        if user.id == self.user.id:
            return
        else:
            reactionData[user] = list(reaction.emoji)
            return


def run_bot():
    client = MyClient()
    client.run(botVars.get("token"))


def init():
    import_settings()
    run_bot()


if __name__ == "__main__":
    init()
