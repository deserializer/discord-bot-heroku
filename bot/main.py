import os
from discord.ext import commands

bot = commands.Bot(command_prefix="!")
TOKEN = os.getenv("DISCORD_TOKEN")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}({bot.user.id})")

@bot.event()
async def on_ready():
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game('Labymod')

if __name__ == "__main__":
    bot.run(TOKEN)
