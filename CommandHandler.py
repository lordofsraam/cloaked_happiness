import time, sys, os
from twisted.python import log

class BasicUser():
	def __init__(self, user):
		self.nick = user.split('!', 1)[0]
		self.real = user.split('!', 1)[1].split('@', 1)[0]
		self.user = user.split('!', 1)[1].split('@', 1)[1]

class Ship:
    Engines = False #on or off
    Docked = True
    Location = "Earth"
    Commander = "lordofsraam"
    Fuel = 100 #percent
    LaunchReady = False
    PortLatch = True
    StarboardLatch = True

commands = {}

officers = []

class CommandHandler():
	""" This class handles all the commands sent in private messages """

	def __init__(self, bot, command, user, channel):
		self.command = command
		self.bot = bot
		self.channel = channel
		self.user = BasicUser(user)
		self.COMMANDS = {
			"you are dismissed": self.dismissed,
			"who are you": self.whoami,
			"what are you": self.whoami,
			"ship status": self.shipstat,
			"ship's status": self.shipstat,
			"engines": self.engines,
			"an officer": self.crew,
			"where are": self.whereami,
			"prepare to launch": self.launchseq,
			"prep to launch": self.launchseq,
			"undock": self.dockoff,
			"disengage from dock": self.dockoff,
			"who is in charge": self.commander,
		}
		self.HandleCommand()

	def reply(self, msg):
		self.bot.msg(self.channel, msg.encode('utf-8'))

	def HandleCommand(self):
		params = self.command.strip().split()
		command = self.command.split(':')[1].strip()
		#params_eol
		#command = params[0].lower()


		for c in self.COMMANDS:
			if c in command:
				try:
					self.COMMANDS[c](params)
				except IndexError:
					self.reply("Human interface translation system encountered a syntactical error.")
				except:
					self.reply("Partial AI core corruption occured.")
				return

#####################################################################################

	def commander(self, params):
               	self.reply("The current commander of this ship is "+Ship.Commander)

	def dismissed(self, params):
		if self.user.nick.upper() == Ship.Commander.upper():
		    self.reply("Yes, sir. Have a good day, sir.")
		    reactor.stop()
		else:
		    self.reply("I am sorry, "+self.user.nick+", but only the Commander can dismiss me.")

	def whoami(self, params):
		self.reply("I am an AI created to make space travel in this ship easier.")
		self.reply("My commanding officer, and the captain of this ship, is "+Ship.Commander)

	def shipstat(self, params):
		self.reply("Running diagnostics checks on the ship...")
		if Ship.Engines:
		    self.reply("Engines are up and running, sir.")
		else:
		    self.reply("Engines are off.")
		self.reply("Fuel charges are at %d%% percent."%Ship.Fuel)
		self.whereami(params)

	def engines(self, params):
		if self.user.nick in officers or self.user.nick == Ship.Commander:
		    if "ON" in self.command.upper():
			if Ship.Engines:
			    self.reply( "The engines are already running, sir.")
			else:
			    self.reply( "Warming up the engines.")
			    Ship.Engines = True
		    elif "OFF" in self.command.upper():
			if not Ship.Engines:
			    self.reply( "The engines are already off, sir.")
			else:
			    self.reply( "Cooling down the engines.")
			    Ship.Engines = False
		else:
		    self.reply("Only the Commander or an officer may issue this command.")

	def crew(self, params):
		print self.command
		if "as an officer" in self.command.lower():
		    if self.user.nick.upper() == Ship.Commander.upper():
			self.reply("Yes, sir.")
			officers.append(self.command.split(" ")[-4])
		elif "an officer" in self.command.lower() and "is" in self.command.lower():
		    if self.command.split(" ")[-3] in officers:
			self.reply("Yes, that person is an officer of this ship.")

	def whereami(self, params):
		if Ship.Docked:
		    self.reply("We are currently docked at "+Ship.Location)
		else:
		    self.reply("We are currently at "+Ship.Location)

	def launchseq(self, params):
		if self.user.nick in officers or self.user.nick == Ship.Commander:
		    self.reply("Yes, sir. Running launch sequence.")
		    if Ship.Engines and Ship.Fuel >= 50 and not Ship.Docked:
			self.reply("Sequence succeeded. The ship is ready to launch.")
			Ship.LaunchReady = True
		    else:
			self.reply("Sir, there were errors during the launch procedure check.")
		else:
		    self.reply("Only the Commander or an officer may issue this command.")

	def dockoff(self, params):
		if self.user.nick in officers or self.user.nick == Ship.Commander:
		    if "port" in self.command.lower():
			self.reply("Using manual override to force the latches.")
			if random.randint(0,1000) > 100:
			    self.reply("Port latches clear.")
			else:
			    self.reply("The port-side latches are broken, sir, but the ship is clear.")
		    elif "starboard" in self.command.lower():
			self.reply("Using manual override to force the latches.")
			if random.randint(0,1000) > 100:
			    self.reply("Starboard latches clear.")
			else:
			    self.reply("The starboard-side latches are broken, sir, but the ship is clear.")
		    else:
			self.reply("Disengaging from dock.")
			if random.randint(0,1000) > 10:
			    self.reply("Starboard latches clear.")
			else:
			    self.reply("Starboard-side latches are jammed, sir.")
			    return
			if random.randint(0,1000) > 10:
			    self.reply("Port latches clear.")
			    return
			else:
			    self.reply("Port-side latches are jammed, sir.")
			Ship.Docked = False
			self.reply("Ship now fully disengaged from the dock, sir.")
		else:
		    self.reply("Only the Commander or an officer may issue this command.")


