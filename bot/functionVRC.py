import datetime
from datetime import date
from datetime import timedelta 
from data_voilerc import *
import re
from lxml import etree
from classesVRC import *
from functionVRC import *

xmlfile='D:\DiscordVRC\\testVRC.xml'


def isvaliddate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%d/%m/%y')
        return 1
    except:
        return 0
def isvalidtime(date_text):
    try:
        datetime.datetime.strptime(date_text, '%H:%M')
        myheure=heure.split(':')
        if int(myheure[0])>23:return 0
        elif int(myheure[1])>59:return 0
        else:return 1
    except:
        return 0
def ispast(mydate):
    today=datetime.date.today()
    mynewdate=datetime.date(int("20"+mydate[4:6]),int(mydate[2:4]),int(mydate[0:2]))
    return mynewdate < today
def isvalidlake(lakename=None):
    """prend en entré un nom de lac
    renvoit 1 si'il existe dans la liste
    0 sinon"""
    for ip, lake in enumerate(lakelist):
        for nom in lake.values():
            if str(lakename).lower() in str(nom).lower(): return 1
    return 0
def readlakename(lakename=None):
    for ip, lake in enumerate(lakelist):
        for nom in lake.values():
            if str(lakename).lower() in str(nom).lower(): return lakelist[ip]["Name"]
    return 0
def readregion(lakename=None):
    for ip, lake in enumerate(lakelist):
        for nom in lake.values():
            if str(lakename).lower() in str(nom).lower(): return lakelist[ip]["Region"]
    return 0
def readville(lakename=None):
    for ip, lake in enumerate(lakelist):
        for nom in lake.values():
            if str(lakename).lower() in str(nom).lower(): return lakelist[ip]["Ville"]
    return 0
def readmap(lakename=None):
    for ip, lake in enumerate(lakelist):
        for nom in lake.values():
            if str(lakename).lower() in str(nom).lower(): return lakelist[ip]["Map"]
    return 0
def ischannelexist(ctx, lakename=None, mydate=None):
    curcategory = ctx.channel.category
    date = datetime.datetime.strptime(mydate, "%d/%m/%y")
    if date.day < 10: daystr="0"+str(date.day) 
    else: daystr=str(date.day)
    if date.month < 10: monthstr="0"+str(date.month)
    else: monthstr=str(date.month)
    yearstr=str(date.year)[-2:]
    for nom in curcategory.channels:
        if daystr+monthstr+yearstr+"_"+lakename.lower() in nom.name: return 1
    return 0
def isvalidcreatechannel(ctx):
    curcategory = ctx.channel.category.name
    curchannel = ctx.channel.name
    if re.match('NAVIGATION_[A-Z]*', curcategory) and curchannel=='créer_rencontre':return 1
    else: return 0
def isvalidnavchannel(channel):
    if re.match('[0-9]*_[0-9][0-9][0-9][0-9][0-9][0-9]_[a-z]*', channel.name):return 1
    else: return 0
def isaddnavmessage(message):
    if re.match('\+[0-9] [0-9]*\:[0-5][0-9]', message.content): 
        if isvalidnavchannel(message.channel):return 1
        else: return 0
    else: return 0
def isremovenavmessage(message):
    if re.match('\-[0-9] [0-9]*\:[0-5][0-9]', message.content): 
        if isvalidnavchannel(message.channel):return 1
        else: return 0
    else: return 0     
def addnav(message):
    chan=message.channel.name
    total=int(chan[:chan.find("_")])
    total=total+int(message.content[1:message.content.find(" ")])
    newchan=str(total)+chan[chan.find("_"):]
    return newchan
def formatheure(heure):
    myheure=heure.split(':')
    if len(myheure[0])==1:myheure[0]="0"+myheure[0]
    if len(myheure[1])==1:myheure[1]="0"+myheure[1]
    return myheure[0]+":"+myheure[1]


            