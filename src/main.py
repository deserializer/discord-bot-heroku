import os
from discord.ext import commands

bot = commands.Bot(command_prefix='!')
TOKEN = os.getenv('DISCORD_TOKEN')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}(id:{bot.user.id})')

bot.run(TOKEN)