# 28-Apr-2012
# wibblemyflibble@gmail.com
# reallyrose
# Python IRCEirtaBot
# Probably useless, poor thing.

# http://cdn.memegenerator.net/instances/400x/19655931.jpg

import time, socket, sys, string, re, random, datetime, string, urllib2, GoodUrlList
from collections import defaultdict
from random import choice


# Global variables - a necessary evil:

TheChosen  =  eval ( open ( 'TheChosen.txt' ).read () ) # People that can do special things
IgnoreUser =  eval ( open ( 'IgnoreUser.txt' ).read () ) # People to be ignore by the bot
botnick    =  '127.0.0.1'
channel    =  '#xmas'
#channel   =  '#testbot'
password   =  ''
port       =  6667
server     =  '127.0.0.1'


# Connecting to a server:

irc = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
irc.connect ( ( server, port ) )

print irc.recv ( 4096 )


# Set nick

irc.send ( 'NICK ' + botnick + '\r\n' )
irc.send ( 'USER ' + botnick + ' ' + botnick + ' ' + botnick + ' :BeepBeep\r\n' )

running = True



# Many Functions, fun for all the family:

def Volunteer (): # For potential volunteers

	global User

	irc.send (
          'PRIVMSG ' + User +
          ' : Why not become one of the awesome Green Shirts for xxxxxx! http://xxxxxx.com/volunteer \r\n'
        )

	irc.send (
          'PRIVMSG ' + User +
          ' : If you have questions, highlight rooose or reallyrose (Just say the name into chat) or if she isn\'t here, email volunteer@xxxxxx.com \r\n'
        )

def Quit (): # only quit when I say so

	global TheChosen

	QUser = data [ 1:data.find ( '!' ) ] #Slice

	if QUser in TheChosen:

		irc.send (
                  'PRIVMSG ' + channel +
                  ' :I have to leave, bye-bye :( \r\n'
                )

		irc.send ( 'QUIT\r\n' )

		global running

		running = False # quit program

	else:
		irc.send ( 'PRIVMSG ' + channel + ' :Only Goshujin-sama can tell me to do that, desu.\r\n' ) # if not...
		
def GreetNew (): # Greet new users

	global IgnoreUser
	global User

	if data.find ( 'JOIN ' ) != -1:

		if User in IgnoreUser:

			pass

		else:

			irc.send (
                          'PRIVMSG ' + channel +
                          ' :Welcome to ' + channel + ', ' + User + '\r\n'
                        )
			
def RandAnime (): # Select a random anime from a pre-determined list. List is stored in a .py file in the same folder.

	random.seed

	AnimeNum = random.choice ( GoodUrlList.GoodList )
	AnimeSite = 'http://myanimelist.net/anime/%s' % AnimeNum

	req = urllib2.Request ( url = AnimeSite )

	f = urllib2.urlopen ( req )

	scrape = f.read ()

	title = ' '.join ( re.findall ( '<title>.*</title>', scrape ) )
	title = title.replace ( '<title>', '' ).replace ( '</title>', '' )

	synoptitle = ' '.join ( re.findall ( '<td valign="top"><h2>Synopsis</h2>.*<br />', scrape ) )
	synoptitle = synoptitle.replace ( '<td valign="top"><h2>Synopsis</h2>', '' ).replace ( '<br />', '' )

	f.close

	irc.send (
          'PRIVMSG ' + channel +
          ' :Why not try this? ' + AnimeSite + '\r\n'
        )

	irc.send (
          'PRIVMSG ' + channel +
          ' :' + title + '\r\n'
        )

	irc.send (
          'PRIVMSG ' + channel +
          ' :' + synoptitle + '\r\n'
        )

	
def Fact (): # function to pull a random fact picture from a list of facts in a txt file

	FactFile = 'FactDict.txt'
	FactFile = eval ( open ( FactFile ).read () )

	random.seed

	PickFact = random.choice ( FactFile )

        # post it

	irc.send (
          'PRIVMSG ' + channel +
          ' :' + PickFact + ' Fact! \r\n'
        )

def Cat (): # function to pull a random cat picture from a dictionary of cat pictures in a txt file

	CatFile = 'CatDict.txt'
	CatFile = eval ( open ( CatFile ).read () )

	random.seed

	PickCat = random.choice ( CatFile )

        # post it

	irc.send (
          'PRIVMSG ' + channel +
          ' :Kitteh! =^_^= ' + PickCat + '\r\n'
        )
	
def Countdown (): # Count # days til xxxxxx!

	diff = datetime.datetime ( 2012, 11, 9 ) - datetime.datetime.today ()

	date = str ( diff.days )

	irc.send (
          'PRIVMSG ' + channel +
          ' :Just ' + date + ' days til xxxxxx 2012! \r\n'
        )

def FactAdd (): # write link to txt file

	global data

	LinkFile = open ( 'FactLog.txt', 'a' )
	LinkFile.write ( data )
	LinkFile.close ()

        # let user know link has been stored

	irc.send (
          'PRIVMSG ' + channel +
          ' :Your fact has been stored, desu!\r\n'
        )

def Committee (): # If someone wants someone from the committee

	irc.send (
          'PRIVMSG ' + channel +
          ' :If you wait a bit, someone from the committee might be here. If not, email addresses are here! http://xxxxxx.com/committee :D \r\n'
        )

def Help (): # Halp!

	if data.find ( '!help' ) != -1:

		irc.send (
                  'PRIVMSG ' + channel +
                  ' :!committee - If you\'re looking for the committee!, !fact - interesting facts, !AddFact <fact> - Add a fact to Lori, !countdown - countdown to xxxxxx, !pre-reg - pre-reg info, !volunteer - info on how to volunteer, !cat - provides a cat, !anime - provides an anime suggestion. Quality not guaranteed. \r\n'
                )
	

# Core code

while running:

	data = irc.recv ( 4096 )

	User = data [ 1:data.find ( '!' ) ] # Slice

	GreetNew ()

	if data.find (
          'Follow synIRC on Twitter! http://twitter.com/synirc - Now looking for feedback on how we can improve the user experience. Tweet us your ideas!'
        ) != -1: # Don't join chan til server has finished spamming

		irc.send ( 'JOIN ' + channel + '\r\n' )

	if data.find ( 'End of /NAMES list.' ) != -1: # don't reg til joined chan

		irc.send ( 'PRIVMSG nickserv IDENTIFY ' + password + ' \r\n' )

	if data.find ( 'PING' ) != -1: # ping/pong server

		irc.send ( 'PONG ' + data.split () [ 1 ] + '\r\n' )

	elif data.find ( '!LoriBot Quit' ) != -1:

		Quit ()

	elif re.findall ( '^:reallyrose', data ) or re.findall ( '^:rooose', data ) and data.find ( 'Bad LoriBot' ) != -1:

		irc.send (
                  'PRIVMSG ' + channel +
                  ' :\001ACTION is sorry. LoriBot will be good in future ;_; \001\r\n'
                )

	elif re.findall ( '^:reallyrose', data ) or re.findall ( '^:rooose', data ) and data.find ( 'Good LoriBot' ) != -1:

		irc.send (
                  'PRIVMSG ' + channel +
                  ' :~Waaaiii!~ \001ACTION is a happy bot. =^_^= \001\r\n'
                )

	elif data.find ( ':!anime' ) != -1:

		if User == 'SomeUser': # This is for a regular who likes pokemon. 1 out 5 times he asks for anime, he will get pokemon

			PokeList = (
                          527, 1118, 11019, 11009, 1119, 1564, 9107, 10740, 12671, 9917, 2363, 1525, 1565, 10302, 5529, 1120, 5256, 2842,
			  6275, 8438, 6178, 11073, 4795, 1122, 4026, 1121, 1526, 13799, 1709, 6877, 4793, 11069, 7550, 5844, 8709, 6555,
			  4910, 4794, 4792, 11853, 5845, 5526, 4874, 10916, 10917, 2201, 6385, 528, 1527, 1117, 2847, 7695
                        )

			random.seed ()

			PokeNum = random.randint ( 1, 5 )

			if PokeNum == 1:

				PokeRand = random.choice ( PokeList )

				irc.send (
                                  'PRIVMSG ' + channel +
                                  ' :Why not try this? http://myanimelist.net/anime/%s \r\n'
                                ) % PokeRand

			else:

				RandAnime ()

		if User == 'SomeOtherUser': # This is for another regular, who likes LoGH. 2 out 5 times he asks for anime, he will get LoGH

			LOGHList = (
                          820, 3371, 3015, 3014, 3016, 3665
                        )

			random.seed ()

			LOGHNum = random.randint ( 1, 5 )

			if LOGHNum == 1:

				LOGHRand = random.choice ( LOGHList )

				irc.send (
                                  'PRIVMSG ' + channel +
                                  ' :Why not try this? http://myanimelist.net/anime/%s \r\n'
                                ) % LOGHRand

			if LOGHNum == 3:

				irc.send (
                                  'PRIVMSG ' + channel +
                                  ' :Why not try this? http://tinyurl.com/dyvam6j \r\n'
                                )

			else:

				RandAnime ()

		else:

			RandAnime ()

	elif re.findall ( channel + ' :!fact', data ):

		Fact ()

	elif re.findall ( channel + ' :!AddFact', data ):

		FactAdd ()

	elif re.findall ( channel + ' :!addfact', data ):

		FactAdd ()

	elif data.find ( channel + ' :!countdown' ) != -1:

		Countdown ()

	elif data.find ( channel + ' :!pre-reg' ) != -1: # Pre-reg command.

		irc.send (
                  'PRIVMSG ' + User +
                  ' :Pre-reg for xxxxxx 2012 here! http://xxxxxx.com/prereg \r\n'
                )

	elif data.find ( channel + ' :!committee' ) != -1:

		Committee ()

	elif data.find ( channel + ' :!cat' ) != -1:

		Cat ()

	elif data.find ( channel + ' :!volunteer' ) != -1:

		Volunteer ()

	elif data.find ( channel + ' :!help' ) != -1:

		Help ()

	print data