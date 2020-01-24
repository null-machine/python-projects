import discord
import asyncio
from chatterbot import ChatBot
from chatterbot.conversation import Statement
from chatterbot.trainers import UbuntuCorpusTrainer

# id 551378788286464000
# token NTUxMzc4Nzg4Mjg2NDY0MDAw.D1wTew.yGnbvpNyxcg7GM5PF6CBMQ2Gx0Q
# perms 68608
# https://discordapp.com/api/oauth2/authorize?client_id=551378788286464000&scope=bot&permissions=68608

token = 'NTUxMzc4Nzg4Mjg2NDY0MDAw.D1wTew.yGnbvpNyxcg7GM5PF6CBMQ2Gx0Q'
client = discord.Client()

chatbot = ChatBot(
	'bhot',
	logic_adapters=[
		'chatterbot.logic.BestMatch',
		'chatterbot.logic.MathematicalEvaluation'
	],
	initialize=True
)

trainer = UbuntuCorpusTrainer(chatbot)
trainer.train()

async def verify(response, trigger):
	
	await response.add_reaction('🤠')
	
	def check(reaction, user):
		return user != response.author and reaction.message.id == response.id
	try:
		reaction, user = await client.wait_for('reaction_add', timeout=20.0, check=check)
	except asyncio.TimeoutError:
		# await message.clear_reactions()
		await response.edit(content=response.content + ' ~')
		chatbot.learn_response(Statement(text=response.content), trigger)
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
		response = await message.channel.send(chatbot.get_response(message.content))
		await verify(response, trigger)
	
client.run(token)
