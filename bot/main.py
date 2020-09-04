import discord, os, server
from discord.ext import commands
import urllib.parse, urllib.request, re, webbrowser

#UptimeRobot is being weird, so i'm using GitHub to take this code and host it on Heroku.
#boost my server at https://discord.gg/6GPjN8C
prefix="cs!"

client = commands.Bot(command_prefix=prefix)
token = os.getenv("DISCORD_TOKEN")

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
  await client.change_presence(activity=discord.Game(name="cs!help || made with <3 by Syntax Corp"))

@client.event
async def on_message(message):
  
  msg = message.content.lower()
  
  if message.author == client.user:
    return
  
  elif msg.startswith("cs!hello"):
    await message.channel.send(f"hello, @{message.author}!")
  
  elif msg.startswith("cs!help"):
    await message.channel.send("commands: cs!hello, cs!replsearch <query>, cs!twitch <query>, cs!youtube <query>, cs!google <query>")
  
  elif msg.startswith("cs!replsearch "):
    resultr = msg.split('cs!replsearch ', 1)
    if resultr[-1] == "":
      await message.channel.send("Error :face_with_raised_eyebrow:, no query given")
    else:
      await message.channel.send(f"https://replsearch.johndo3.repl.co/results?q={replaceSpaces(resultr[-1])}")

  elif msg.startswith("cs!replsearch"):
    await message.channel.send("Error :face_with_raised_eyebrow:, no query given")
  
  elif msg.startswith("cs!twitch "):
    resultt = msg.split('cs!twitch ', 1)
    if resultt[-1] == "":
      await message.channel.send("Error :face_with_raised_eyebrow:, no query given")
    else:
      await message.channel.send(f"https://twitch.tv/search?term={replaceSpaces(resultt[-1])}")

  elif msg.startswith("cs!twitch"):
    await message.channel.send("Error :face_with_raised_eyebrow:, no query given")

  elif msg.startswith("cs!youtube "):
    resulty = msg.split('cs!youtube ', 1)
    if resulty[-1] == "":
      await message.channel.send("Error :face_with_raised_eyebrow:, no query given")
    else:
      await message.channel.send(f"https://www.youtube.com/results?search_query={replaceSpaces(resulty[-1])}")

  elif msg.startswith("cs!youtube"):
    await message.channel.send("Error :face_with_raised_eyebrow:, no query given")

  elif msg.startswith("cs!google "):
    result = msg.split('cs!google ', 1)
    if result[-1] == "":
      await message.channel.send("Error :face_with_raised_eyebrow:, no query given")
    else:
      await message.channel.send(f"https://www.google.com/search?q={replaceSpaces(result[-1])}")

  elif msg.startswith("cs!google"):
    await message.channel.send("Error :face_with_raised_eyebrow:, no query given")
  
  elif msg.startswith("cs!"):
    await message.channel.send("Error :face_with_raised_eyebrow:, not a valid command")

server.server()
client.run(token)