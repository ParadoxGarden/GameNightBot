import discord

botVars = dict()
bannedWords = list()


def importSettings():
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
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        author = message.author
        content = message.content
        channel = message.channel
        prefixLength = len(botVars.get("prefix"))

        # we do not want the bot to reply to itself
        if author.id == self.user.id:
            return

        for word in bannedWords:
            if word.lower() in content.lower():
                await message.delete()
                await channel.send("Boop!")
                await author.send(
                    "Sorry friend, you used a banned word, the word was \"" +
                    word + "\". if you feel this was done in error, please contact an administrator")
                return ""

        if message.content[:prefixLength] == (botVars.get("prefix")):
            realContent = message.content[prefixLength:]
            if realContent == "help":
                print("")


def runBot():
    client = MyClient()
    client.run(botVars.get("token"))


def main():
    importSettings()
    runBot()


if __name__ == "__main__":
    main()
