import discord
import asyncio
# from chatterbot import ChatBot
# from chatterbot.conversation import Statement
# from chatterbot.trainers import UbuntuCorpusTrainer

# id 551378788286464000
# perms 68608

token = 'NTUxMzc4Nzg4Mjg2NDY0MDAw.XHp1gw.52YL0UzlIHdEdTGOBhRgn07UHgg'

client = discord.Client()

# chatbot = ChatBot(
# 	'bhot',
# 	logic_adapters=[
# 		'chatterbot.logic.BestMatch',
# 		'chatterbot.logic.MathematicalEvaluation'
# 	],
# 	initialize=True
# )
#
# trainer = UbuntuCorpusTrainer(chatbot)
# trainer.train()

async def verify(response, trigger):
	
	await response.add_reaction('🤠')
	
	def check(reaction, user):
		return user != response.author and reaction.message.id == response.id
	try:
		reaction, user = await client.wait_for('reaction_add', timeout=20.0, check=check)
	except asyncio.TimeoutError:
		# await message.clear_reactions()
		pass
	else:
		await response.delete()
	

@client.event
async def on_ready():
	print(f'logged in as {client.user}')

@client.event
async def on_message(message):
	if message.author != client.user:
		trigger = message.content
		response = await message.channel.send('test')
		await verify(response, trigger)
	
client.run(token)
