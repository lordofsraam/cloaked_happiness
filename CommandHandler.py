import time, sys, os, random, re
from twisted.python import log
from twisted.internet import reactor

class BasicUser():
	def __init__(self, user):
		self.nick = user.split('!', 1)[0]
		self.real = user.split('!', 1)[1].split('@', 1)[0]
		self.user = user.split('!', 1)[1].split('@', 1)[1]

class Status:
	Stable = "Stable"
	Ready = "Ready"
	Auto = "Auto"
	Overheated = "Overheated"
	Malfunctioning = "Malfunctioning"
	Damaged = "Damaged"
	Off = "Off"

class Ship:
    Engines = False #on or off
    Docked = True
    Location = "Earth"
    Commander = "lordofsraam"
    Fuel = 100 #percent
    LaunchReady = False
    PortLatch = True
    StarboardLatch = True
    Thrusters = Status.Off

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
			r"^you[\s]+are[\s]+dismissed": self.dismissed,
			r"^(who|what)[\s]+are[\s]+you": self.whoami,
			r"^(ship|ship(\'s|s))[\s]+status": self.shipstat,
			r"^engines": self.engines,
			r"an[\s]+officer": self.crew,
			r"^where[\s]+are": self.whereami,
			r"^(prepare|prep)[\s]+(to|for)[\s]+launch": self.launchseq,
			r"^undock": self.dockoff,
			r"^disengage[\s]+from[\s]+dock": self.dockoff,
			r"^who[\s]+is[\s]+in[\s]+charge": self.commander,
		}
		self.HandleCommand()

	def reply(self, msg):
		self.bot.msg(self.channel, msg.encode('utf-8'))

	def HandleCommand(self):
		params = self.command.strip().split()
		command = re.sub(r'^%s[:,.\s]+' % (self.bot.nickname), "", self.command)
		params_eol = []
		for i, s in enumerate(params):
			params_eol.append(u" ".join(params[i::]))

		for c in self.COMMANDS:
			#if c in command:
			if re.search(c, command, re.IGNORECASE) != None:
				try:
					self.COMMANDS[c](params, params_eol)
				except IndexError:
					self.reply("Human interface translation system encountered a syntactical error.")
				except:
					self.reply("Partial AI core corruption occured.")
					raise
				return

#####################################################################################

	def commander(self, params, params_eol):
               	self.reply("The current commander of this ship is "+Ship.Commander)

	def dismissed(self, params, params_eol):
		if self.user.nick.upper() == Ship.Commander.upper():
		    self.reply("Yes, sir. Have a good day, sir.")
		    reactor.stop()
		else:
		    self.reply("I am sorry, "+self.user.nick+", but only the Commander can dismiss me.")

	def whoami(self, params, params_eol):
		self.reply("I am an AI created to make space travel in this ship easier.")
		self.reply("My commanding officer, and the captain of this ship, is "+Ship.Commander)

	def shipstat(self, params, params_eol):
		self.reply("Running diagnostics checks on the ship...")
		if Ship.Engines:
		    self.reply("Engines are up and running.")
		else:
		    self.reply("Engines are off.")
		self.reply("Fuel charges are at %d%% percent."%Ship.Fuel)
		if Ship.PortLatch and Ship.StarboardLatch:
			self.reply("All docking latches are functional.")
		else:
			if not Ship.StarboardLatch: self.reply("Starboard docking latch is malfunctioning.")
			if not Ship.PortLatch: self.reply("Port docking latch is malfunctioning.")
		self.reply("Thrusters report status: "+Ship.Thrusters)
		self.whereami(params, params_eol)

	def engines(self, params, params_eol):
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

	def crew(self, params, params_eol):
		print self.command
		if "as an officer" in self.command.lower():
		    if self.user.nick.upper() == Ship.Commander.upper():
			self.reply("Yes, sir.")
			officers.append(self.command.split(" ")[-4])
		elif "an officer" in self.command.lower() and "is" in self.command.lower():
		    if self.command.split(" ")[-3] in officers:
			self.reply("Yes, that person is an officer of this ship.")

	def whereami(self, params, params_eol):
		if Ship.Docked:
		    self.reply("We are currently docked at "+Ship.Location)
		else:
		    self.reply("We are currently at "+Ship.Location)

	def launchseq(self, params, params_eol):
		if self.user.nick in officers or self.user.nick == Ship.Commander:
		    self.reply("Yes, sir. Running launch sequence.")
		    if Ship.Engines and Ship.Fuel >= 50 and not Ship.Docked and Ship.Thrusters != Status.Off:
				self.reply("Sequence succeeded. The ship is ready to launch.")
				Ship.LaunchReady = True
		    else:
				self.reply("Sir, there were errors during the launch procedure check.")
		else:
		    self.reply("Only the Commander or an officer may issue this command.")

	def dockoff(self, params, params_eol):
		if self.user.nick in officers or self.user.nick == Ship.Commander:
		    if "port" in self.command.lower():
				self.reply("Using manual override to force the latches.")
				if random.randint(0,1000) > 20:
				    self.reply("Port latches clear.")
				else:
				    self.reply("The port-side latches are broken, sir, but the ship is clear.")
				    Ship.PortLatch = False
				    Ship.Docked = False
		    elif "starboard" in self.command.lower():
				self.reply("Using manual override to force the latches.")
				if random.randint(0,1000) > 20:
				    self.reply("Starboard latches clear.")
				else:
				    self.reply("The starboard-side latches are broken, sir, but the ship is clear.")
				    Ship.StarboardLatch = False
				    Ship.Docked = False
		    else:
				self.reply("Disengaging from dock.")
				if random.randint(0,1000) > 10:
				    self.reply("Starboard latches clear.")
				else:
				    self.reply("Starboard-side latches are jammed, sir.")
				    return
				if random.randint(0,1000) > 10:
				    self.reply("Port latches clear.")
				else:
				    self.reply("Port-side latches are jammed, sir.")
				    return
				Ship.Docked = False
				self.reply("Ship now fully disengaged from the dock, sir.")
		else:
		    self.reply("Only the Commander or an officer may issue this command.")


	def thrusters(self, params, params_eol):
		if self.user.nick in officers or self.user.nick == Ship.Commander:
			if "status" in self.command.lower():
				self.reply("Thruster status: "+Ship.Thrusters)
			elif "on" in self.command.lower():
				if Ship.Engines:
					self.reply("Thrusters are on and set to auto-stabalize.")
					Ship.Thrusters = Status.Auto
				else:
					self.reply("Error. Thruster module replied: No power input.")
			elif "off" in self.command.lower():
				Ship.Thrusters = Status.Off
				self.reply("Thrusters succesfully powered down.")
		else:
		    self.reply("Only the Commander or an officer may issue this command.")
