# /\/\/\/\/\/\/\
import discord
import logging

# this fun stuff below makes the bot work
handler = logging.FileHandler(filename='bayonet.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# the actual fun part
@client.event
async def on_ready():
    print(f'Bayonet loaded, logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('.ping'):
        await message.channel.send('pong!')


client.run('x', log_handler=handler, log_level=logging.DEBUG)
# /\/\/\/\/\/\/\