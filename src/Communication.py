import discord
import json
import TTS
import sys

class MyClient(discord.Client):
	async def on_ready(self):
		for guild in self.guilds:
			if guild.name == "Game Night":
				gnguild = guild
		print("printing message: " + sys.argv[2] + " in " + sys.argv[1])
		for channel in gnguild.channels:
			if channel.name == sys.argv[1]:
				await channel.send(sys.argv[2])
		await self.close()


	async def on_message(self, message):
		pass


client = MyClient()
settings = open("settings.json", "r")
key=json.loads(settings.read())
settings.close()
client.run(key["Token"])