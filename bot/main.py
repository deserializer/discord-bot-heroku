# bot.py
import logging
import os
import traceback
from numpy import empty
import discord
from discord.ext.commands import Bot
from discord import Intents
from discord.utils import get
import pandas as pd
import requests
import io
import csv
import os.path
import json, boto3

from discord.ext import tasks
import gspread
from oauth2client.service_account import ServiceAccountCredentials



chestLoggsDict = {}
lootLogger = {}
itemNamesDict = {}
TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.members = True
client = discord.Client()
bot = Bot("!",intents=intents)

def chestLoggs(chestLoggsCvsR):
        for row in chestLoggsCvsR:
            if(row == ['Date', 'Player', 'Item', 'Enchantment', 'Quality', 'Amount']):
                continue
            if(len(row)==6):
                if(True):
                    itemNameConstant = row[2] + '.' + row[3]
                    if(itemNameConstant in chestLoggsDict):
                        chestLoggsDict[itemNameConstant]['itemName'] = itemNameConstant
                        chestLoggsDict[itemNameConstant]['counter'] += int(row[5])
                        chestLoggsDict[itemNameConstant]['depositedBy'].append(row[1])
                        
                        if(row[1] in chestLoggsDict[itemNameConstant]['depositersCounter']):
                            chestLoggsDict[itemNameConstant]['depositersCounter'][row[1]] += int(row[5])
                        else:
                            chestLoggsDict[itemNameConstant]['depositersCounter'][row[1]] = int(row[5])
                    else:
                        chestLoggsDict[itemNameConstant] = {}
                        chestLoggsDict[itemNameConstant]['itemName'] = itemNameConstant
                        chestLoggsDict[itemNameConstant]['enhancement'] = row[3]
                        chestLoggsDict[itemNameConstant]['counter'] = int(row[5])
                        chestLoggsDict[itemNameConstant]['depositedBy']  = [row[1]]
                        chestLoggsDict[itemNameConstant]['depositersCounter']  = {}
                        chestLoggsDict[itemNameConstant]['depositersCounter'][row[1]] = int(row[5])
                else:
                    itemWithdrawn(row)

        # return chestLoggsDict use it

def getItemNames():
    client = boto3.client('s3',
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name = os.getenv("REGION_NAME")
    )
    resource = boto3.resource(
        's3',
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name = os.getenv("REGION_NAME")
    )
    obj = client.get_object(
        Bucket = os.getenv("S3_BUCKET"),
        Key = os.getenv("S3_FILE_NAME")
    )
    lines = obj['Body'].read().decode('utf-8').splitlines(True)
    data = csv.reader(lines, delimiter=';')
    for row in data:
        rowString = row[0].split(':',2)
        if(len(rowString) !=3):
            itemNamesDict[rowString[1].rstrip().lstrip()] = ""
        else:
            itemNamesDict[rowString[1].rstrip().lstrip()] = rowString[2].lstrip().rstrip()
    return itemNamesDict

def getLootLogger(logLoggerCvsR):
    itemName = {}
    itemName = getItemNames()
    obj = {}
    obj['looters'] = []
    for row in logLoggerCvsR:
        enhancement = 0
        enhancementList = row[2].split('@')
        if(len(enhancementList)>1):
            enhancement = enhancementList[1]
        itemNameConstant = itemName[row[2]] + '.' + str(enhancement)
        if(itemNameConstant in lootLogger ):
            lootLogger[itemNameConstant]['itemName'] = itemNameConstant
            lootLogger[itemNameConstant]['counter'] +=1 
            lootLogger[itemNameConstant]['looters'].append(row[1])
                
                
            if(row[1] in lootLogger[itemNameConstant]['lootersCounter']):
                lootLogger[itemNameConstant]['lootersCounter'][row[1]] += 1
            else:
                lootLogger[itemNameConstant]['lootersCounter'][row[1]] = int(row[3])
                    
        else:
            lootLogger[itemNameConstant] = {}
            lootLogger[itemNameConstant]['itemName'] = itemNameConstant
            lootLogger[itemNameConstant]['enhancement'] = enhancement
            lootLogger[itemNameConstant]['counter'] = int(row[3])
            lootLogger[itemNameConstant]['looters']  = [row[1]]
            lootLogger[itemNameConstant]['lootersCounter']  = {}
            lootLogger[itemNameConstant]['lootersCounter'][row[1]] = int(row[3])
    # return lootLogger    

def checker():
    itemPartialyMissing = {}
    itemNotInChest = []
    for i in lootLogger:#loop through item in logger
        if( i in chestLoggsDict):
            itemPartialyMissing = countByLooters(i,itemPartialyMissing)
        else:
            itemNotInChest.append(lootLogger[i])
    return itemNotInChest, itemPartialyMissing
         
def countByLooters(i,itemPartialyMissing):
    itemPartialyMissing[i] = {}
    itemPartialyMissing[i]['itemName'] = i
    itemPartialyMissing[i]['left'] = {}
    for j in lootLogger[i]['lootersCounter']:
        if(j in chestLoggsDict[i]['depositersCounter']):
            #deduct how many was dropped
            left = lootLogger[i]['lootersCounter'][j] - chestLoggsDict[i]['depositersCounter'][j]
            if(left>0):
                itemPartialyMissing[i]['left'][j] = left
                
        
    return itemPartialyMissing

@bot.event
async def on_ready():
    print('Bot is ready.')
    #getSpreadsheetData.start()
    

@bot.command(pass_context=True)
async def test(ctx, *args):

    found = False
    server = ctx.message.guild
    # role_name = (' '.join(args))
    guild = ctx.guild
    wantedRole  = None
    role: discord.Role = discord.utils.get(ctx.message.guild.roles, name=' '.join(args))

    if(role not in server.roles):
        await ctx.send("Role doesn't existtt")
    else:
        if(role.members != []):
            await ctx.send("Members Under " + role.name + " are:" )
            for member in role.members:
                await ctx.send(member.name)
        else:
            await ctx.send("No Members Under " + role.name)
    await ctx.send("Command executed")

"""
This is responsible to get all memebers in a certain channel that have heals role
"""
@bot.command(pass_context=True)
async def healer(ctx, *args):
    healerRoles = ['|          Healing           |','Elite Healer (All)','1350+ Blight','1350+ Fallen','1350+ Hallowfall','1350+ Wild']
    channel: discord.Channel = discord.utils.get(ctx.message.guild.channels, name=' '.join(args))
    if channel.members == []:
        await ctx.send("No Users in " + ' '.join(args) + " Voice Channel")
        return
    await ctx.send("Members who have the healer role are: ")
    for member in channel.members:
        for role in member.roles:
            if( role.name in healerRoles):
                await ctx.send(member.name)
                break
    await ctx.send("Command executed")
    
"""
This is responsible to get all memebers in a certain channel that have Tank role
"""
@bot.command(pass_context=True)
async def tank(ctx, *args):
    healerRoles = ['|          Tank             |','Elite Tank (All)','1350+ Hand of Justice','1350+ Camlann','1350+ Grovekeeper','1350+ Grailseeker','1350+ Mace','1350+ Soulscythe','1350+ Morningstar',
                   '1350+ Oathkeepers']
    channel: discord.Channel = discord.utils.get(ctx.message.guild.channels, name=' '.join(args))
    if channel.members == []:
        await ctx.send("No Users in " + ' '.join(args) + " Voice Channel")
        return
    await ctx.send("Members who have the healer role are: ")
    for member in channel.members:
        for role in member.roles:
            if( role.name in healerRoles):
                await ctx.send(member.name)
                break
    await ctx.send("Command executed")
    
"""
This is responsible to get all memebers in a certain channel that have Support role
"""
@bot.command(pass_context=True)
async def support(ctx, *args):
    healerRoles = ['|          Support          |','Elite Support (All)','1350+ Enigmatic','1350+ Lifecurse','1350+ Locus','1350+ Glacial']
    channel: discord.Channel = discord.utils.get(ctx.message.guild.channels, name=' '.join(args))
    if channel.members == []:
        await ctx.send("No Users in " + ' '.join(args) + " Voice Channel")
        return
    await ctx.send("Members who have the Support role are: ")
    for member in channel.members:
        for role in member.roles:
            if( role.name in healerRoles):
                msg = await ctx.send(member.name)
                await msg.add_reaction("❌")
                reaction = get(msg.reactions, emoji ="❌")
                await ctx.send(reaction)
                break
    await ctx.send("Command executed")
    

        
@bot.command(pass_context=True)
async def chest(ctx):
    x = ''
    # itemPartialyMissing = {}
    # itemNotInChest = []
    urlDic = {}
    chestLoggsDict.clear()
    lootLogger.clear()
    for url in ctx.message.attachments:
        urlSplit = url.url.split('/')
        urlName = urlSplit[len(urlSplit)-1]
        urlDic[urlName] = url
        
    if('chestLog.txt' not in urlDic.keys() or 'lootLogger.csv' not in urlDic.keys()):
        await ctx.send("Wrong files uploaded.")
        return
    
    
    file_requestChestLog = None
    chestLoggsCvsR = None
    file_requestChestLog = requests.get(urlDic['chestLog.txt']).content.decode('utf-8')
    chestLoggsCvsR = csv.reader(file_requestChestLog.splitlines(), delimiter='\t')
    
    file_requestLogger = None
    logLoggerCvsR = None
    file_requestLogger = requests.get(urlDic['lootLogger.csv']).content.decode('utf-8')
    logLoggerCvsR = csv.reader(file_requestLogger.splitlines(), delimiter=';')
    
    
    
    
    try:
        chestLoggs(chestLoggsCvsR)
    except Exception as e:
        logging.error(traceback.format_exc())
        msg = await ctx.send("Error with chestLog File")
        return
    try:
        getLootLogger(logLoggerCvsR)
    except Exception as e:
        logging.error(traceback.format_exc())
        msg = await ctx.send("Error with lootLogger File")
        return

    itemNotInChest, itemPartialyMissing = checker()
    if(itemPartialyMissing!=[]):
        # msg = await ctx.send("Item Partially Missing")
        y = ''
        firstBlock = True
        for i in itemPartialyMissing:   
            if(itemPartialyMissing[i]['left']!={}):
                if(firstBlock):
                    y = "**Item Partially Missing**"
                    firstBlock = False
                yBefore = str(y)
                y = y + '\n' + str(itemPartialyMissing[i])
                if(len(y)>2000):
                    y = yBefore
                    msg = await ctx.send(y)
                    await msg.add_reaction("❌")
                    y = ''
                    y = y + '\n' + str(itemPartialyMissing[i])
        if(y!=''):
            msg = await ctx.send(y)
            await msg.add_reaction("❌")
    if(itemNotInChest!=[]):
        # await ctx.send("Item That was never banked")
        x = ''
        firstBlock = True
        for i in itemNotInChest:
            if(firstBlock):
                x = "**Item That was never banked**"
                firstBlock = False
            xBefore = x
            x = x + '\n' + "Item Name: " + str(i['itemName']) + '. LootersCounter: ' + str(i['lootersCounter'])
            if(len(x)>2000):
                x = xBefore
                msg = await ctx.send(x)
                await msg.add_reaction("❌")
                x = ''
                x = x + '\n' + "Item Name: " + str(i['itemName']) + '. LootersCounter: ' + str(i['lootersCounter'])
        msg = await ctx.send(x)
        await msg.add_reaction("❌")
    # await ctx.send("Done")


        
@bot.command()
async def testing(ctx):
    msg = await ctx.send("test")
    await msg.add_reaction("❌")
    reaction = get(msg.reactions, emoji ="❌")
    await ctx.send(reaction)
    # await msg.delete()
    
@bot.event
async def on_raw_reaction_add(payload):
    message = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
    reaction = discord.utils.get(message.reactions, emoji="❌")
    if reaction.count >=2:
        await message.delete()

    
@bot.command()
async def commands(ctx):
    await ctx.send("To look a certain role on a user for a spesfic channel use the !X Y. Where X is the name of the role(healer,support,tank) and Y is the name of the channel")
    await ctx.send("To use the logger checker type !chest and attach the chest logs and lootlogger, name of files matter. lootLogger.csv and chestLog.txt. Chest logs should not have header. Loot logger can be uploaded as it is")

#Spreasheet Related Code:

#Creating a player object
class player:
    def __init__(self,name,discordID):
        self.name = name
        self.roles = []
        self.weapons = []
        self.discordID = discordID


#Automated task that updates the data in the bot every x minutes, won't run if not enabled in line 146
#Won't run for now, needs a credentials.json file
@tasks.loop(minutes=15)
async def getSpreadsheetData():
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1A3Sjs3aqUZjFFlRCw6HqbCMMxzmEtQtesRPjCoSLFBQ/edit#gid=0').worksheet("Sheet1")
    allvalues = sheet.get_all_values()
    #Seperating the list of lists returned by the line above
    upperRow = allvalues[0]
    weapons = allvalues[1]
    players = allvalues[2:]

    category = ""

    #Creating a player object for each player and adding them to a list
    global listofplayers
    listofplayers = []
    for v in players:
        if (v[0]!="" and " " not in v[0]):
            p = player(v[0])
            
            #Determining current role
            if upperRow[i].split(" ")[0] != "":
                        category =  upperRow[i].split(" ")[0]

            #Assigning weapons to players
            for i in range (len(v)):
                if v[i]=="YES":
                    p.weapons.append(weapons[i])

                    #Assigning current role to player
                    if not category in p.roles:
                        p.roles.append(category)

            listofplayers.append(p)

#Calls the function above, enables the possibility of a manual update
@bot.command(aliases=['upd'])
async def updatestats(ctx):
    await getSpreadsheetData()

#The commands below create and send an embed that shows players of the healer,tank,support and dps roles on the selected voice channel.
#Below each player's name appear all the weapons they can play according to the spreadsheet
@bot.command(aliases=["heals"])
async def healersOnVoice(ctx,*,args = None):
    if args == None:
        await ctx.send("Missing arguments, no Voice Channel selected")
    else:
        healerList = []
        global listofplayers
        for p in listofplayers:
            if ("Healer" in p.roles):
                healerList.append(p)

        if healerList == []:
            await ctx.send("No healers found in the list, are you sure the data in the bot is up to date with the spreadsheet?")
        else:
            healersOnComms = []
            channel: discord.Channel = discord.utils.get(ctx.message.guild.channels, name=args)
            if channel != None:
                if channel.members == []:
                    await ctx.send("No Users in Voice Channel '" + args + "'")
                    return
                else:
                    for member in channel.members:
                        for h in healerList:
                            if str(member.id) == str(h.discordID):
                                healersOnComms.append(h)

                embed = discord.Embed(title=':ambulance:  Healers on ' + args + '  :ambulance: ',description="",colour=discord.Colour.green())
                embed.set_thumbnail(url="https://cdn3.iconfinder.com/data/icons/weapon-mmorpg-game/100/Staff-14-512.png")
                #Footer
                embed.set_footer(text = "made with love by 123xd")
                
                for healer in healersOnComms:
                    weaponsString = ""
                    for weapon in healer.weapons:
                        weaponsString = weaponsString + weapon + ", "
                    weaponsString = weaponsString[:-2]
                    embed.add_field(name=healer.name,value=weaponsString)

                await ctx.send(embed=embed)
            else:
                await ctx.send("Channel not found")

@bot.command(aliases=["tanks"])
async def tanksOnVoice(ctx,*,args = None):
    if args == None:
        await ctx.send("Missing arguments, no Voice Channel selected")
    else:
        TankList = []
        global listofplayers
        for p in listofplayers:
            if ("Tank" in p.roles):
                TankList.append(p)

        if TankList == []:
            await ctx.send("No Tanks found in the list, are you sure the data in the bot is up to date with the spreadsheet?")
        else:
            tanksOnComms = []
            channel: discord.Channel = discord.utils.get(ctx.message.guild.channels, name=args)
            if channel != None:
                if channel.members == []:
                    await ctx.send("No Users in Voice Channel '" + args + "'")
                    return
                else:
                    for member in channel.members:
                        for x in TankList:
                            if str(member.id) == str(x.discordID):
                                tanksOnComms.append(x)

                embed = discord.Embed(title=':shield:  Tanks on ' + args + '  :shield:',description="",colour=discord.Colour.blue())
                embed.set_thumbnail(url="https://cdn0.iconfinder.com/data/icons/game-20/64/online_game_weapon_fight_equipment-05-256.png")
                #Footer
                embed.set_footer(text = "made with love by 123xd")

                for tank in tanksOnComms:
                    weaponsString = ""
                    for weapon in tank.weapons:
                        weaponsString = weaponsString + weapon + ", "
                    weaponsString = weaponsString[:-2]
                    embed.add_field(name=tank.name,value=weaponsString)

                await ctx.send(embed=embed)
            else:
                await ctx.send("Channel not found")
    
@bot.command(aliases=["supps"])
async def suppsOnVoice(ctx,*,args = None):
    if args == None:
        await ctx.send("Missing arguments, no Voice Channel selected")
    else:
        supportList = []
        global listofplayers
        for p in listofplayers:
            if ("Support" in p.roles):
                supportList.append(p)

        if supportList == []:
            await ctx.send("No Supports found in the list, are you sure the data in the bot is up to date with the spreadsheet?")
        else:
            suppsOnComms = []
            channel: discord.Channel = discord.utils.get(ctx.message.guild.channels, name=args)
            if channel != None:
                if channel.members == []:
                    await ctx.send("No Users in Voice Channel '" + args + "'")
                    return
                else:
                    for member in channel.members:
                        for x in supportList:
                            if str(member.id) == str(x.discordID):
                                suppsOnComms.append(x)

                embed = discord.Embed(title=':tools:  Supports on ' + args + '  :tools:',description="",colour=discord.Colour.gold())
                embed.set_thumbnail(url="https://cdn3.iconfinder.com/data/icons/weapon-mmorpg-game/100/Staff-15-512.png")
                #Footer
                embed.set_footer(text = "made with love by 123xd")
                
                for supp in suppsOnComms:
                    weaponsString = ""
                    for weapon in supp.weapons:
                        weaponsString = weaponsString + weapon + ", "
                    weaponsString = weaponsString[:-2]
                    embed.add_field(name=supp.name,value=weaponsString)

                await ctx.send(embed=embed)
            else:
                await ctx.send("Channel not found")

@bot.command(aliases=["dps"])
async def dpsOnVoice(ctx,*,args = None):
    if args == None:
        await ctx.send("Missing arguments, no Voice Channel selected")
    else:
        dpsList = []
        global listofplayers
        for p in listofplayers:
            if ("DPS" in p.roles):
                dpsList.append(p)

        if dpsList == []:
            await ctx.send("No DPS found in the list, are you sure the data in the bot is up to date with the spreadsheet?")
        else:
            dpsOnComms = []
            channel: discord.Channel = discord.utils.get(ctx.message.guild.channels, name=args)
            if channel != None:
                if channel.members == []:
                    await ctx.send("No Users in Voice Channel '" + args + "'")
                    return
                else:
                    for member in channel.members:
                        for x in dpsList:
                            if str(member.id) == str(x.discordID):
                                dpsOnComms.append(x)

                embed = discord.Embed(title=':crossed_swords:  DPS on ' + args + '  :crossed_swords:',description="",colour=discord.Colour.red())
                embed.set_thumbnail(url="https://cdn2.iconfinder.com/data/icons/sports-161/100/Fencing-256.png")
                #Footer
                embed.set_footer(text = "made with love by 123xd")

                for dps in dpsOnComms:
                    weaponsString = ""
                    for weapon in dps.weapons:
                        weaponsString = weaponsString + weapon + ", "
                    weaponsString = weaponsString[:-2]
                    embed.add_field(name=dps.name,value=weaponsString)

                await ctx.send(embed=embed)
            else:
                await ctx.send("Channel not found")

#Something like a "sign up" command that when used adds the user's discord id to the correct row
@bot.command()
async def confirm(ctx,nameInSpreadsheet = None):
    global listofplayers
    usernameList = []
    for p in listofplayers:
        usernameList.append(p.name)

    if nameInSpreadsheet == None:
        await ctx.send("Missing arguments, please type in your AO username")
    elif nameInSpreadsheet not in usernameList:
        await ctx.send("Username not found in the spreadsheet, please make sure you typed your username correctly and try again")
    else:
        scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
        client = gspread.authorize(creds)

        sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1A3Sjs3aqUZjFFlRCw6HqbCMMxzmEtQtesRPjCoSLFBQ/edit#gid=0').worksheet("Sheet1")
        allvalues = sheet.get_all_values()

        i=1
        for value in allvalues:
            if value[0] == nameInSpreadsheet:
                break
            else:
                i+=1

        sheet.update_cell(i, 28, str(ctx.author.id))
        await ctx.send("Confirmation Success for " + nameInSpreadsheet)

#These need to be adjusted if they are to be useful
@bot.command()
async def weapons(ctx,player):
    global listofplayers
    print("WEAPONS:")
    for p in listofplayers:
        if (player == p.name):
            print(p.weapons)

@bot.command()
async def roles(ctx,player):
    global listofplayers
    print("ROLES:")
    for p in listofplayers:
        if (player == p.name):
            print(p.roles)
    
bot.run(TOKEN)

"""
Done:
    * show all members under a certain role. 
    * list all memebers in X voice comms that have certain roles [all tanks roles], [all healrs roles], [all supports role]
    * Logger
"""

