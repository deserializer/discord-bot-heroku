#Lark2002's Tarkov Challenge Generator V0.01
import discord
from discord.ext import commands
import os
import random
client = commands.Bot(command_prefix = "!")
def weaponchoose():
    weapcat = ["AR", "Carbines", "LMGs", "SMGs", "Shotguns", "DMR", "Snipers", "Pistols"]
    AR = ["ADAR 2-15", "AK-101", "AK-102", "AK-103", "AK-104", "AK-105", "AK-74", "AK-74M", "AK-74N", "AK-74MS", "AK-74MSN", "AKS-74", "AKS-74N", "AKS-74U", "AKS-74UN", "AKS-74UB", "ASh-12", "DT-MDR 5.56x45", "DT MDR .308", "HK 416A5", "Kel-Tec RFB", "M4A1", "SA-58", "TX-15 DML", "Vepr AKM/VPO"]
    Carbines = ["AS VAL", "OP-SKS", "SKS", "Vepr Hunter/VPO-101"]
    LMGs = ["RPK-16"]
    SMGs = ["MP5", "MP5K-N", "MP7","MP9","MPX","P90","PP-19-01 Vityaz-SN","PP-9 Klin","PP-9 Kedr","PPSH-41","Saiga-9"]
    Shotguns = ["590A1","M870","MP-133","MP-153","Saiga-12","TOZ-106","KS-23M"]
    DMR = ["M1A","RSASS","SR-25","SVDS","VSS Vintorez"]
    Snipers = ["DVL-10","M700","Moisin","Moisin Inf","SV-98","T-5000","VPO-215"]
    Pistols = ["APB","APS","FN 5-7","GLOCK17","GLOCK18C","M1911A1","M45A1","M9A3","MP-443 Grach","P226R","PB Pistol","PM Pistol","SR-1MP","TT Pistol"]
    weapcatchoice = random.choice(weapcat)
    if weapcatchoice == "AR":
        gun = random.choice(AR)
    elif weapcatchoice ==  "Carbines":
        gun = random.choice(Carbines)
    elif weapcatchoice == "LMGs":
        gun = random.choice(LMGs)
    elif weapcatchoice == "SMGs":
        gun = random.choice(SMGs)
    elif weapcatchoice == "Shotguns":
        gun = random.choice(Shotguns)
    elif weapcatchoice == "DMR":
        gun = random.choice(DMR)
    elif weapcatchoice == "Snipers":
        gun = random.choice(Snipers)
    elif weapcatchoice == "Pistols":
        gun = random.choice(Pistols)
    return gun
def armorchoose():
    armclass = ["c2","c3","c4","c5","c6"]
    c2 = ["Module-3M Armor", "Paca(Lol)","6B2"]
    c3 = ["MF-UNTAR","Zhuk-3 Press Armor","6B23-1","BNTI Kirasa"]
    c4 = ["Highcom Trooper","6B13 Assault","6B23-2 Armor"]
    c5 = ["BNTI Korund-VM","FORT Redut-M","Killa Armor","IOTV Gen4 (High Mobility)","BNTI Gzehl-K","FORT Defender-2","IOTV Gen4 (Assault)","IOTV Gen4 (Full)","FORT Redut-T5"]
    c6 = ["Slick Plate Carrier","Zhuk-6a","6B43 Zabralo-Sh"]
    armclasschoice = random.choice(armclass)
    if armclasschoice == "c2":
        armor = random.choice(c2)
    elif armclasschoice == "c3":
        armor = random.choice(c3)
    elif armclasschoice == "c4":
        armor = random.choice(c4)
    elif armclasschoice == "c5":
        armor = random.choice(c5)
    elif armclasschoice == "c6":
        armor = random.choice(c6)
    return armor
def helmetchoose():
    helmetclass = ["c1","c2","c3","c4","c5","c6"]
    c1 = ["Tac-Kek Fast MT Helmet (non-ballistic replica)","Soft tank crew helmet TSH-4M-L"]
    c2 = ["Kolpak-1S riot helmet","SHPM Firefighter's helmet","PSH-97 Djeta helmet","Jack-o'-lantern tactical pumpkin helmet"]
    c3 = ["UNTAR helmet","6B47 Ratnik-BSh Helmet","LZSh light helmet","SSh-68 helmet (Penis Helm)","Kiver-M Helmet","DEVTAC Ronin ballistic helmet","SSSh-95 Sfera-S (Sphere-S)"]
    c4 = ["MSA ACH TC-2001 MICH Series Helmet","MSA ACH TC-2002 MICH Series Helmet","MSA Gallet TC 800 High Cut combat helmet","Highcom Striker ACHHC IIIA helmet","ZSh-1-2M helmet","Highcom Striker ULACH IIIA helmet","Diamond Age Bastion Helmet","Ops-Core Fast MT SUPER HIGH CUT Helmet","Crye Precision Airframe Tan","Team Wendy EXFIL Ballistic Helmet","Galvion Caiman Ballistic Helmet","BNTI LSHZ-2DTM Helmet","Killa Helmet"]
    c5 = ["Altyn helmet","Rys-T helmet"]
    c6 = ["Vulkan-5 (LShZ-5) heavy helmet"]
    helmetclasschoice = random.choice(helmetclass)
    if helmetclasschoice == "c1":
        helmet = random.choice(c1)
    elif helmetclasschoice == "c2":
        helmet = random.choice(c2)
    elif helmetclasschoice == "c3":
        helmet = random.choice(c3)
    elif helmetclasschoice == "c4":
        helmet = random.choice(c4)
    elif helmetclasschoice == "c5":
        helmet = random.choice(c5)
    elif helmetclasschoice == "c6":
        helmet = random.choice(c6)
    return helmet


#answers with a weapon choice
@client.command()
async def weapon(ctx):
    choice = weaponchoose()
    embed = discord.Embed(
        color= discord.Color.dark_purple()
    )
    embed.set_author(name="Your weapon choice is:")
    embed.add_field(name=choice, value="Good Luck Soldier, You'll Need It",inline = False)
    await ctx.send(embed=embed)


#answers with an armor choice
@client.command()
async def armor(ctx):
    choice = armorchoose()
    embed = discord.Embed(
        color= discord.Color.dark_purple()
    )
    embed.set_author(name="Your armor choice is:")
    embed.add_field(name=choice, value="You may as well wear a paper bag",inline = False)
    await ctx.send(embed=embed)

#answers with a helmet choice
@client.command()
async def helmet(ctx):
    choice = helmetchoose()
    attachments = random.choice(["Yes","No"])
    embed = discord.Embed(
        color= discord.Color.dark_purple()
    )
    embed.set_author(name="Your helmet choice is:")
    embed.add_field(name=choice, value="It won't help, but it might make you 'feel' safe.", inline=False)
    embed.add_field(name="Can you add attachments?", value=attachments,inline = False)
    await ctx.send(embed=embed)
#creates a loadout
@client.command()
async def loadout(ctx):
    armorchoice = armorchoose()
    weapchoice = weaponchoose()
    helmchoice = helmetchoose()
    embed = discord.Embed(
        color= discord.Color.dark_purple()
    )
    embed.set_author(name="Your loadout is:")
    embed.add_field(name="Weapon:", value=weapchoice,inline = False)
    embed.add_field(name="Armor:", value=armorchoice, inline=False)
    embed.add_field(name="Helmet:", value=helmchoice, inline=False)
    await ctx.send(embed=embed)
#help command
@client.command()
async def help(ctx):
    embed = discord.Embed(
        color= discord.Color.dark_purple()
    )
    embed.set_author(name="Help : list of commands available")
    embed.add_field(name="!weapon", value="Will choose a weapon for you",inline = False)
    embed.add_field(name="!armor:", value="Will choose armor for you", inline=False)
    embed.add_field(name="!helmet:", value="Will choose a helmet for you", inline=False)
    embed.add_field(name="!loadout:", value="Will choose a full loadout for you", inline=False)
    await ctx.send(embed=embed)
TOKEN = os.getenv("DISCORD_TOKEN")

client.run(TOKEN)
