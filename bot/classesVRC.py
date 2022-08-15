import time
import datetime
import re
import discord
from functionVRC import *
from lxml import etree

xmlfile='D:\DiscordVRC\\testVRC.xml'

class PARTICIPANT:
    def __init__(self, nbparticipant, participant):
        self.nb=nbparticipant
        self.name=participant

class RDV:
    def __init__(self, heure, nbparticipant, participant):
        self.heure=formatheure(heure)
        self.nbparticipant=nbparticipant
        self.participantlist=[PARTICIPANT(nbparticipant, participant)]
    
    def addParticipant(self, nbparticipant, participant):
        self.nbparticipant=self.nbparticipant + nbparticipant
        for myparticipant in self.participantlist:
            if myparticipant.name == participant:
                myparticipant.nb+=nbparticipant
                return
        newparticipant=PARTICIPANT(nbparticipant, participant)
        self.participantlist.append(newparticipant)

    def removeParticipant(self, nbparticipant, participant):
        for myparticipant in self.participantlist:
            if myparticipant.name == participant:
                if nbparticipant < myparticipant.nb:
                    myparticipant.nb-=nbparticipant
                    self.nbparticipant-=nbparticipant
                else:
                    self.participantlist.remove(myparticipant)
                    self.nbparticipant-=myparticipant.nb
                    nbparticipant=myparticipant.nb
            else:nbparticipant=0
        return nbparticipant
        
class NAVIGATION:
    def __init__(self, nbparticipants, day, month, year, fulllakename, channel):
        self.lake=fulllakename
        self.region=readregion(self.lake)
        self.ville=readville(self.lake)
        self.map=readmap(self.lake)
        self.date=day+month+year
        self.totparticipants=nbparticipants
        self.channel=channel
        self.embedmsg=None
        self.rdvs=[]


    def takeHour(self,rdv):
        return rdv.heure
        
    def addParticipant(self, heure, nbparticipant, participant):
        if self.rdvs!=[]:
            existrdv=0
            for rdv in self.rdvs:
                if rdv.heure==formatheure(heure):
                    rdv.addParticipant(nbparticipant, participant)
                    self.addparticipanttoxml(rdv.heure, nbparticipant, participant)
                    existrdv=1
            if not existrdv:
                newrdv=RDV(heure, nbparticipant, participant)
                self.rdvs.append(newrdv)
                self.addrdvtoxml(heure, nbparticipant, participant)
        else:
            newrdv=RDV(heure, nbparticipant, participant)
            self.takeHour(newrdv)
            self.rdvs.append(newrdv)
            self.addrdvtoxml(heure, nbparticipant, participant)
        self.totparticipants=self.totparticipants+nbparticipant
        self.rdvs.sort(key=self.takeHour)
        self.embed()
        
    def removeParticipant(self, heure, nbparticipant, participant):
        if self.rdvs!=[]:
            existrdv=0
            for rdv in self.rdvs:
                if rdv.heure==formatheure(heure):
                    nbremove=rdv.removeParticipant(nbparticipant, participant)
                    if rdv.nbparticipant<1:self.rdvs.remove(rdv)    
                    existrdv=1
            if existrdv:
                self.totparticipants-=nbremove
                self.rdvs.sort(key=self.takeHour)
                self.embed()
                self.removeparticipantfromxml(heure, nbparticipant, participant)
                
    def embed(self):
        """ Retourne un embed formaté pour être lu par discord"""
        embed = discord.Embed(title="Rencontre navigation "+self.lake+" le "+self.date[0:2]+"/"+self.date[2:4]+"/"+self.date[4:6])
        field = "Region: "+self.region+"\n"
        field += "Ville: "+self.ville+"\n"
        field += "Lieu: "+self.lake+"\n"
        field += "map: "+self.map+"\n"
        field += "Total participants: "+str(self.totparticipants)+"\n"
        embed.add_field(name="test field", value=field)
        footer=""
        for rdv in self.rdvs:
            footer += "["+rdv.heure+"]\n"
            for participant in rdv.participantlist:
                footer += str(participant.nb)+" "+participant.name+"\n"
            footer +="\n"
        embed.set_footer(text=footer)
        return embed
    
    def addnavtoxml(self):
        navigations = etree.parse(xmlfile).getroot()
        navigation=etree.SubElement(navigations, "navigation")
        navigation.set("region", self.region)
        navigation.set("lac", self.lake)
        navigation.set("ville", self.ville)
        navigation.set("date", self.date)
        navigation.set("map", self.map)
        navigation.set("totparticipants", str(self.totparticipants))
        navigation.set("channel", str(self.channel))
        navigation.set("embedmsg", str(self.embedmsg.id))
        with open(xmlfile, 'wb') as f:
            f.write(etree.tostring(navigations, pretty_print=True))
            f.close
    
    def addrdvtoxml(self, heure, nbparticipant, participant):
        navigations = etree.parse(xmlfile).getroot()
        for nav in navigations.xpath("/navigations/navigation[contains(@channel,'"+self.date+"_"+self.lake.lower()+"')]"):
            nav.attrib['totparticipants']=str(self.totparticipants+nbparticipant)
            rendezvous=etree.SubElement(nav, "rdv")
            rendezvous.set("heure", formatheure(heure))
            rendezvous.set("nbparticipant", str(nbparticipant))
            particpants=etree.SubElement(rendezvous, "participants")
            particpants.set("nb", str(nbparticipant))
            particpants.set("participant", participant)
        with open(xmlfile, "wb") as f:
            f.write(etree.tostring(navigations)) 
            f.close()
           
    def addparticipanttoxml(self, heure, nbparticipant, participant):
        navigations = etree.parse(xmlfile).getroot()
        for nav in navigations.xpath("/navigations/navigation[contains(@channel,'"+self.date+"_"+self.lake.lower()+"')]"):
            nav.attrib['totparticipants']=str(self.totparticipants+nbparticipant)
        for rdv in navigations.xpath("/navigations/navigation[contains(@channel,'"+self.date+"_"+self.lake.lower()+"')]/rdv[@heure='"+formatheure(heure)+"']"):
            nbrdv=int(rdv.get("nbparticipant"))
            rdv.attrib['nbparticipant']=str(nbrdv+nbparticipant)
            isexistpart=0
            for part in rdv:
                if part.get("participant")==participant:
                    isexistpart=1
                    nbpart=int(part.get("nb"))
                    part.attrib['nb']=str(nbpart+nbparticipant)
            if not isexistpart:
                participant=etree.SubElement(rdv, "participants")
                participant.set("nb", nbparticipant)
                participant.set("participant", participant)
        with open(xmlfile, "wb") as f:
            f.write(etree.tostring(navigations)) 
            f.close()

    def removeparticipantfromxml(self, heure, nbparticipant, participant):
        navigations = etree.parse(xmlfile).getroot()
        for rdv in navigations.xpath("/navigations/navigation[contains(@channel,'"+self.date+"_"+self.lake.lower()+"')]/rdv[@heure='"+formatheure(heure)+"']"):
            nbrdv=int(rdv.get("nbparticipant"))
            isexistpart=0
            for part in rdv:
                if part.get("participant")==participant:
                    isexistpart=1
                    nbpart=int(part.get("nb"))
                    if nbpart<nbparticipant:nbparticipant=nbpart
                    if nbpart-nbparticipant==0:part.getparent().remove(part)
                    else:
                        part.attrib['nb']=str(nbpart-nbparticipant)
            if isexistpart:
                rdv.attrib['nbparticipant']=str(nbrdv-nbparticipant)
                if nbrdv-nbparticipant==0:rdv.getparent().remove(rdv)
                for nav in navigations.xpath("/navigations/navigation[contains(@channel,'"+self.date+"_"+self.lake.lower()+"')]"):
                    nav.attrib['totparticipants']=str(self.totparticipants)
        with open(xmlfile, "wb") as f:
            f.write(etree.tostring(navigations)) 
            f.close()    

    def removenavfromxml(self):
        navigations = etree.parse(xmlfile).getroot()
        for nav in navigations.xpath("/navigations/navigation[contains(@channel,'"+self.date+"_"+self.lake.lower()+"')]"):
            nav.getparent().remove(nav)
        with open(xmlfile, "wb") as f:
            f.write(etree.tostring(navigations)) 
            f.close()    


class CHAN:
    def __init__(self, reg, date, cat, chan):
        self.region=reg
        self.date=self.englishDate(date)
        self.category=cat
        self.channel=chan
        self.position=0
        
    def englishDate(self, date):
        myday=date[0:2]
        mymonth=date[2:4]
        myyear=date[4:6]
        return myyear+mymonth+myday

class CHANLIST:
    def __init__(self):
        self.sorted=0
        self.chanlist=[]

    def addChan(self, chan):
        self.chanlist.append(chan)
        self.sorted=0
    
    def removeChan(self, chan):
        self.chanlist.remove(chan)
        self.sorted=0

    def sortKeyReg(self, chan):
        return chan.region

    def sortKeyDate(self, chan):
        return chan.date

    def sortList(self):
        if self.chanlist != []:
            self.chanlist.sort(key=self.sortKeyDate)
            self.chanlist.sort(key=self.sortKeyReg)
            regpreced=''
            position=7
            for chan in self.chanlist:
                if regpreced=='':
                    chan.position=position
                    regpreced=chan.region
                elif chan.region==regpreced:
                    position+=1
                    chan.position=position
                else:
                    position=7
                    regpreced=chan.region
                    chan.position=position
            self.sorted=1