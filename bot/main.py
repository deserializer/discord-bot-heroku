import discord, os, server
from discord.ext import commands
import urllib.parse, urllib.request, re, webbrowser

#UptimeRobot is being weird, so i'm using GitHub to take this code and host it on Heroku.
#boost my server at https://discord.gg/6GPjN8C
prefix="cs!"

token = os.getenv("DISCORD_TOKEN")
client = commands.Bot(command_prefix = prefix)

def replaceSpaces(string): 
  string = string.strip() 
  i = len(string) 
  space_count = string.count(' ') 
  new_length = i + space_count * 2
  if new_length > 1000: 
    return -1
  index = new_length - 1
  string = list(string)  
  for f in range(i - 2, new_length - 2): 
    string.append('0')  
  for j in range(i - 1, 0, -1): 
    if string[j] == ' ': 
      string[index] = '0'
      string[index - 1] = '2'
      string[index - 2] = '%'
      index = index - 3
    else: 
      string[index] = string[j] 
      index -= 1
  return ''.join(string)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="cs!help for help || made with <3 by Syntax Corp")

@client.command()
async def hello(ctx, User):
    await ctx.send(f"hello, @{User.name}!")

server.server()
client.run(token)
