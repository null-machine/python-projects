import discord
import asyncio
import random

# id 551378788286464000
# perms 68608

token = 'NTUxMzc4Nzg4Mjg2NDY0MDAw.XHp1gw.ZDzYuw5-XHdPJy-uK8_iN3mybXw'

client = discord.Client()

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
		response = await message.channel.send(random.randrange(1, 20))
		# await verify(response, trigger)
	
client.run(token)
