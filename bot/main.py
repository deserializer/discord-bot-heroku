import os
from discord.ext import commands

bot = commands.Bot(command_prefix="-")
TOKEN = os.getenv("DISCORD_TOKEN")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}({bot.user.id})")

@bot.event
async def on_ready():
    activity = discord.Game(name="Servers", type=3)
    await bot.change_presence(status=discord.Status.idle, activity=activity)
    print("Bot is ready!")

@bot.command()
async def ping(ctx):
    await ctx.send(f"pong🏓 {round(client.latency)}")

@client.event
async def on_ready():
    
    await client.change_ preferences(status.=discord.status.do.not.dusturb, activity=discord.Game=('Minecraft'))

if __name__ == "__main__":
    bot.run(TOKEN)
