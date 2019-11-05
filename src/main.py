import os
from discord.ext import commands

client = commands.Bot(command_prefix='!')
token = os.getenv('DISCORD_TOKEN')

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}(id:{client.user.id})')

client.run(token)