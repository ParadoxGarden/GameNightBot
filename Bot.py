import json
import threading
import time

import discord
import schedule

import TTS


class MyClient(discord.Client):
	def __init__(self, filename, schedule_thread, **options):
		super().__init__(**options)
		self.guild = None
		self.threads = schedule_thread
		settings = open(filename, "r")
		self.bot_variables = json.loads(settings.read())
		self.games = self.bot_variables.get("Games")
		self.voice_engine = TTS.init_voice()
		self.prefix = self.bot_variables["Prefix"]
		settings.close()
	
	async def on_ready(self):
		emoji_names = list()
		for game in self.games:
			emoji_names.append(game.get("Emoji"))
		
		voice_engine_voices = self.voice_engine.getProperty("voices")
		self.voice_engine.setProperty('rate', int(self.bot_variables['TTS']['Rate']))
		self.voice_engine.setProperty('volume', float(self.bot_variables['TTS']['Volume']))
		self.voice_engine.setProperty('voice', voice_engine_voices[int(self.bot_variables['TTS']['Voice'])])
		
		for emoji in self.emojis:
			if emoji.name in emoji_names:
				self.vote_emojis[emoji.name] = emoji
		
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
			return
		
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
				self.begin_voting_period()
			
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
	
	async def collate_votes(self):
		pass
	
	async def begin_voting_period(self):
		for channel in self.guild.text_channels:
			if channel.name == "announcements":
				await channel.send("testing")
	
	async def begin_game_night(self):
		pass


def init_scheduler():
	schedstop = threading.Event()
	
	def timer():
		while not schedstop.is_set():
			schedule.run_pending()
			time.sleep(900000)
	
	schedthread = threading.Thread(target=timer)
	schedthread.start()
	return [schedstop, schedthread]
	schedule.every().tuesday.at("12:00").do(self.begin_voting_period())  # Voting period starts 12pm tuesday
	schedule.every().monday.at("19:00").do(self.collate_votes())  # Collate vote data 7pm monday
	schedule.every().monday.at("20:00").do(self.begin_game_night())  # Game night time 8pm monday


def run_bot():
	schedules = init_scheduler()
	client = MyClient("settings.json", schedules)
	client.run(client.bot_variables["Token"])


if __name__ == "__main__":
	run_bot()
