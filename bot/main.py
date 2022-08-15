import discord
import asyncio
import datetime
import re
import os
import time
import schedule
import classesVRC 
from functionVRC import *
from classesVRC import *
import sys
from discord.ext import commands, tasks
from lxml import etree

Client = discord.Client()
navlist=[]
xmlfile='testVRC.xml'
navchanlist=CHANLIST()



bot = commands.Bot(command_prefix = "!", description = "Bot de Gwenn")

@bot.event
async def on_ready():
    await bot.wait_until_ready()
    server = bot.get_guild(997075942050639922)
    tree = etree.parse(xmlfile)
    for nav in tree.xpath("/navigations/navigation"):
        newnav=NAVIGATION(int(nav.get("totparticipants")),'jj', 'mm', 'yy',nav.get("lac"), nav.get("channel"))
        navxml=nav.get("channel")
        navxml=navxml[navxml.find("_"):]
        for chan in server.channels:
            if chan.name[chan.name.find("_"):] == navxml: newnav.channel=chan        
        newnav.date=nav.get("date")
        embedxml=int(nav.get("embedmsg"))
        messages = await newnav.channel.history(limit=500).flatten()
        for msg in messages:
            if msg.id==embedxml:newnav.embedmsg=msg
        for rdv in nav:
            newrdv=RDV(rdv.get("heure"), 0, 'toto')
            newrdv.participantlist=[]
            for part in rdv:
                newpart=classesVRC.PARTICIPANT(int(part.get("nb")), part.get("participant"))
                newrdv.participantlist.append(newpart)
            newnav.rdvs.append(newrdv)
        navlist.append(newnav)
    
    for nav in navlist:
        chan=CHAN(nav.region, nav.date, nav.channel.category, nav.channel)
        navchanlist.addChan(chan)
    
    updatechan.start()
    cleanupchan.start()
    
    print("Ready !")
    
@bot.event
async def on_message(message):
    if isaddnavmessage(message):
        tabmessage=message.content.split(' ')
        nbparticipant=int(tabmessage[0][1:])
        heure=tabmessage[1]
        author=message.author.name
        #newchan=addnav(message)
        #await message.channel.edit(name=newchan)
        mynav=None
        for nav in navlist:
            if nav.channel == message.channel:mynav=nav
        embedmsg=mynav.embedmsg
        mynav.addParticipant(heure, nbparticipant, author)
        await embedmsg.edit(embed=mynav.embed())
    elif isremovenavmessage(message):
        tabmessage=message.content.split(' ')
        nbparticipant=int(tabmessage[0][1:])
        heure=tabmessage[1]
        author=message.author.name
        mynav=None
        for nav in navlist:
            if nav.channel == message.channel:mynav=nav
        embedmsg=mynav.embedmsg
        mynav.removeParticipant(heure, nbparticipant, author)
        await embedmsg.edit(embed=mynav.embed())
    await bot.process_commands(message)

@bot.command()
async def Bonjour(ctx):
    await ctx.send("Bonjour !")

@bot.command()
async def nav(ctx,lakename=None, mydate=None):
    if isvaliddate(mydate):    
        mytabdate=mydate.split('/')
        myday=mytabdate[0]
        if len(myday)==1:myday="0"+myday
        mymonth=mytabdate[1]
        if len(mymonth)==1:mymonth="0"+mymonth
        myyear=mytabdate[2]
    if not isvalidcreatechannel(ctx):
        await ctx.send("La commande ne peut être exécutée dans ce channel")
    elif not isvalidlake(lakename) or not isvaliddate(mydate):
        await ctx.send("La commande est !nav nom_du_lac jj/mm/aa")
    elif ispast(myday+mymonth+myyear):
        await ctx.send("La date choisie est dans le passé")
    else:
        curchannel = ctx.channel
        guild = ctx.message.guild
        curcategory = ctx.channel.category.name
        splitcategory=curcategory.split('_')
        curregion=splitcategory[len(splitcategory)-1]
        cat = discord.utils.get(guild.categories, name=curcategory)
        fulllakename=readlakename(lakename)
        region=readregion(lakename)
        if region != curregion:
            await ctx.send("Le lieu de navigation n'est pas dans la région de ce channel")    
        elif ischannelexist(ctx, fulllakename, mydate):
            await ctx.send("Il existe déjà une rencontre pour ce lieu et cette date")
        else:
            mychannel = await guild.create_text_channel("0_"+myday+mymonth+myyear+"_"+fulllakename, category=cat)
            newnav=NAVIGATION(0,myday,mymonth,myyear,fulllakename, mychannel)
            navlist.append(newnav)
            newnav.embedmsg=await mychannel.send(embed=newnav.embed())
            newnav.addnavtoxml()
            emoji = '\N{THUMBS UP SIGN}'
            await ctx.message.add_reaction(emoji)
            region= readregion(fulllakename)           
            chan=CHAN(region, myday+mymonth+myyear, cat, mychannel)
            navchanlist.addChan(chan)
            navchanlist.sortList()
            tochgpos=0
            for mychan in reversed(navchanlist.chanlist):
                if mychan.region == region:tochgpos=1
                else:tochgpos=0
                if tochgpos:
                    await mychan.channel.edit(position=mychan.position, sync_permissions=True)
                

@bot.command()
async def InfoServeur(ctx):
    serveur = ctx.guild
    nombreDeChainesTexte = len(serveur.text_channels)
    nombreDeChainesVocale = len(serveur.voice_channels)
    Description_du_serveur = serveur.description
    Nombre_de_personnes = serveur.member_count
    Nom_du_serveur = serveur.name
    message = f"Le serveur **{Nom_du_serveur}** contient *{Nombre_de_personnes}* personnes ! \nLa description du serveur est {Description_du_serveur}. \nCe serveur possède {nombreDeChainesTexte} salons écrit et {nombreDeChainesVocale} salon vocaux."
    await ctx.send(message)

@commands.has_role('admin')
@bot.command()
async def getposition(ctx):
    message = ctx.channel.position
    await ctx.send(message)
    
@commands.has_role('admin')
@bot.command()
async def setposition(ctx, pos):
    await ctx.channel.edit(position=int(pos), sync_permissions=True)
    message = ctx.channel.position
    await ctx.send(message)

@commands.has_any_role('admin', 'modo')
@bot.command()
async def delchan(ctx):
    for nav in navlist:
        chan=nav.channel
        if chan==ctx.channel:
            navlist.remove(nav)
            nav.removenavfromxml()
            for mychan in navchanlist.chanlist:
                if mychan.channel==chan:navchanlist.removeChan(mychan)
            await chan.delete()
            
@commands.has_any_role('admin', 'modo')
@bot.command()
async def delmsg(ctx):
    await ctx.channel.purge(limit=None, check=lambda msg: not msg.pinned and not msg.embeds)

@commands.has_role('admin')
@bot.command()    
async def dumpxml(ctx):
    navigations = etree.Element("navigations")
    for nav in navlist:
        navigation=etree.SubElement(navigations, "navigation")
        navigation.set("region", nav.region)
        navigation.set("lac", nav.lake)
        navigation.set("ville", nav.ville)
        navigation.set("date", nav.date)
        navigation.set("map", nav.map)
        navigation.set("totparticipants", str(nav.totparticipants))
        navigation.set("channel", str(nav.channel))
        navigation.set("embedmsg", str(nav.embedmsg.id))
        for rdv in nav.rdvs:
            rendezvous=etree.SubElement(navigation, "rdv")
            rendezvous.set("heure", rdv.heure)
            rendezvous.set("nbparticipant", str(rdv.nbparticipant))
            for part in rdv.participantlist:
                particpants=etree.SubElement(rendezvous, "participants")
                particpants.set("nb", str(part.nb))
                particpants.set("participant", part.name)
    with open(xmlfile, "wb") as f:
        f.write(etree.tostring(navigations)) 
        f.close()

@commands.has_role('admin')
@bot.command()           
async def test(ctx):
    print('test')

#Scheduled task
@tasks.loop(minutes=15) 
async def updatechan():
    for nav in navlist:
        chan=nav.channel.name
        totpart=int(chan[:chan.find("_")])
        if nav.totparticipants != totpart:
            await nav.channel.edit(name=str(nav.totparticipants)+chan[chan.find("_"):])

@tasks.loop(minutes=240) 
async def cleanupchan():
    for nav in navlist:
        chan=nav.channel
        if ispast(nav.date):
            navlist.remove(nav)
            nav.removenavfromxml()
            await chan.delete()

def takeDate(self, nav):
        mydate=nav.date[4:5]+nav.date[2:3]+nav.date[0:1]
        return mydate
        

        
        
bot.run("OTk3MDc3MjcwMjc3NjYwNzIz.G79Gi3.j1TWencAVb5GXzk66TkuS2NxRXX8TdHPa5cpzY")
