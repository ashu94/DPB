#!/usr/bin/env python
import subprocess
from ytsearch import youtubeSearch
import re
from wiki import wiki
from google import google
import lxml.html
from wolfram import wolfram
from threading import Thread
import time
from Goo_trans import translate
from BeautifulSoup import BeautifulSoup
from chatterbotapi import ChatterBotFactory, ChatterBotType
from weather import setUrl
from cricbuzz import *
import pyodbc
import __future__
from module import *
from test_places import *

lastmessage=None
proc=None
chattybot=True
global flag

factory = ChatterBotFactory()
bot1 = factory.create(ChatterBotType.PANDORABOTS, 'b0dafd24ee35a477')
botsessions={}

#this function somehow works in preventing duplicate messages
def mymessage(message):
	global lastmessage
	if (message==lastmessage):
		return True
	else:
		return False

def callmodule(message,peer,search):
	global flag
	global cursor
	global cnxn
	message=message.lower()
	modules=["wiki","bot","google","math","trans","weather","cricket","youtube","nearby"]  #Add module name here so that the for loop below works
	for module in modules:
		if (message.find(module)==0):
			message=message[len(module)+1:]
			if module=="wiki":
				reply=wiki(message,peer,search,cursor,cnxn)
				print reply
				try:
				  if ("Cannot acces link!" in reply):
					reply="No wikipedia article on that, googling instead\n"+google(message)
					return reply
				except:
				  print"except"
				  
				return None
				  
			if module=="google":
				return google(message)
			if module=="bot":
				message=message.lstrip()
				reply=wolfram(message)
				if (reply=="noidea"):
					reply="tough. I'll google that\n"+google(message)
				return reply
			
			if module=="math":
			      a=eval(compile(message, '<string>', 'eval', __future__.division.compiler_flag))
			      #print a
			      return str(a)
			    
						    
			if module=="trans":
			      result=translate(message)
			      return result
			
			if module=="nearby":
			      print "nearby"
			      m=message.split(",")
			      m1=m[0]
			      print m1
			      try:
				m2=m[1]
				
			      except:
				m2=10000
				print m2
			      places(m1,peer,search,cursor,cnxn,m2)
			      return None
			
			if module=="weather":
			      result=setUrl(message)
			      return result
			    
			if module=="youtube":
			     
			      
			      #print "done"
			      try:
				a=querry(message,peer,search,cursor,cnxn)
				return None
			      except:
				print"else main"
				return None
				  
				     
				 # return module
			     # else:
				  #return result
			    
			if module=="cricket":
			      cric = CricbuzzParser()
			      match = cric.getXml()
                              details = cric.handleMatches(match) #Returns Match details as a Dictionary. Parse it according to requirements.
                              b=''
                              for i in details :
                                     b=b+str(i)
                              #print b 
			      return b
			  
			  
		
	global chattybot
	if chattybot:
		global botsessions
		global bot1
		if peer not in botsessions:
			botsessions[peer]=bot1.create_session()
		reply = botsessions[peer].think(message)
		VALID_TAGS = ['br']
		soup = BeautifulSoup(reply)
		for tag in soup.findAll(True):
			if tag.name not in VALID_TAGS:
				tag.hidden = True
		reply=soup.renderContents()
		reply=reply.replace('<br />','\n')
		return reply

def AI(peer,message,search):
        global flag
        flag = 0
	#uncomment for debug
	#if lastmessage is not None:
	#	print 'message is '+message+' and lastmessage is '+lastmessage+'\n'
	if mymessage(message):
		return
	replyrequired=False
	reply=None
	#if group is None:
	replyrequired=True
	if (message[:3].lower()=="bot"):
		replyrequired=True
	reply=callmodule(message,peer,search)
	if((message[:4]=="http") and (message.find(' ')==-1)):
		t = lxml.html.parse(message)
		reply = t.find(".//title").text
		
	#if ((replyrequired==True) and (reply is None)):
		#reply="underconstruction"
	if reply is not None :
		search1=search
		msg(peer,reply,search1)
	
		
		
def db_connect():
    global cursor
    global cnxn
    dsn = ''	#fill credential
    user = ''
    password = ''
    database = ''
 
    con_string = 'DSN=%s;UID=%s;PWD=%s;DATABASE=%s;' % (dsn, user, password, database)
    cnxn = pyodbc.connect(con_string)
    cursor = cnxn.cursor()


def spam(message):
	if (message == lastmessage):
		return True
	else:
		return False

	
def msg(peer,message,search):
	global proc
	global cursor
	global cnxn
	#if (group is not None):
	#	message=peer.split(' ')[0] + ": " + message
	#	peer=group
	if (not spam(message)):
		if(('\n' in message)or('\r' in message) or ('\r\n' in message)):
			tempfile='temp'
			temp=open(tempfile,'w')
			temp.write(message)
			temp.close()
			print message
			cursor.execute("insert into dbo.search_result(search_id, user_id, result) values ( ?, ?, ?)", search, peer, message)
			cnxn.commit()
			#proc.stdin.write('send_text '+peer.replace(' ','_')+' '+tempfile+'\n')
		else:
			print message.replace(' ','_')
			cursor.execute("insert into dbo.search_result(search_id, user_id, result) values ( ?, ?, ?)", search, peer, message)
			cnxn.commit()
			
		cursor.execute(""" UPDATE dbo.bot_search_querry SET flag = 1 where search_id = ?""", [search])
		cnxn.commit()
			#proc.stdin.write('msg '+peer.replace(' ','_')+' '+message+'\n')
		global lastmessage
		lastmessage=message

def bot():
	db_connect()
	global pathtotg
	global proc
	global cursor
	lastmessage=None
	multiline=False
	peer=None
	message=None
	try:
	    while 1 :
	      cursor.execute("select search_id, keyword, user_id, flag from dbo.bot_search_querry where flag = 0")
	      rows = cursor.fetchall()

	      for row in rows:
		search = row.search_id
		peer = row.user_id
		message = row.keyword
		try:
		    AI(peer,message,search)
		    
		except:
		    msg(peer,"Can you please repeat",search)
	except IndexError:
		print "Error: Change colour levels"
	
	
def main():
	botthread = Thread(target = bot)
	botthread.start()
	
	
	botthread.join()

if __name__ == "__main__":
    main()
