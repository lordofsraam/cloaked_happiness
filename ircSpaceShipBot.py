# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.


"""
An example IRC log bot - logs a channel's events to a file.

If someone says the bot's name in the channel followed by a ':',
e.g.

    <foo> logbot: hello!

the bot will reply:

    <logbot> foo: I am a log bot

Run this script with two arguments, the channel name the bot should
connect to, and file to log to, e.g.:

    $ python ircLogBot.py test test.log

will log channel #test to the file 'test.log'.

To run the script:

    $ python ircLogBot.py <channel> <file>
"""


# twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

#custom imports
import markov
import CelestialBodies

# system imports
import time, sys, random, re, string

commands = {}
complex_commands = {}

officers = []

class Ship:

    def __init__(self):
        self.Engines = False #on or off
        self.Docked = True
        self.Orbiting = False
        self.Location = CelestialBodies.Planet()
        self.Commander = "lordofsraam"
        self.FuelAmount = 10000.0
        self.FuelCapacity = 10000.0
        self.LaunchReady = False
        self.Money = 500

    def FuelPercent(self):
        return (self.FuelAmount / self.FuelCapacity) * 100

    def FuelNeededToLaunch(self):
        fuelNeeds = self.Location.Mass() / 50.0
        if self.Location.Atmosphere:
            fuelNeeds = fuelNeeds * 1.5
        return fuelNeeds


TheShip = Ship()


def dismissed(self, user, channel, msg):
    if user.upper() == TheShip.Commander.upper():
        self.msg(channel,"Yes, sir. Have a good day, sir.")
        reactor.stop()
    else:
        self.msg(channel,"I am sorry, "+user+", but only the Commander can dismiss me.")


def whoami(self, user, channel, msg):
    self.msg(channel,"I am an AI created to make space travel in this ship easier.")
    self.msg(channel,"My commanding officer, and the captain of this ship, is "+TheShip.Commander)


def shipstat(self, user, channel, msg):
    self.msg(channel,"Running diagnostics checks on the ship...")
    if TheShip.Engines:
        self.msg(channel,"Engines are up and running, sir.")
    else:
        self.msg(channel,"Engines are off.")
    self.msg(channel,"Fuel charges are at %d%% percent."%TheShip.FuelPercent())
    whereami(self, user, channel, msg)


def engines(self, user, channel, msg):
    if user in officers or user == TheShip.Commander:
        if "ON" in msg.upper():
            if TheShip.Engines:
                self.msg(channel, "The engines are already running, sir.")
            else:
                self.msg(channel, "Warming up the engines.")
                TheShip.Engines = True
        elif "OFF" in msg.upper():
            if not TheShip.Engines:
                self.msg(channel, "The engines are already off, sir.")
            else:
                self.msg(channel, "Cooling down the engines.")
                TheShip.Engines = False
    else:
        self.msg(channel,"Only the Commander or an officer may issue this command.")


def crew(self, user, channel, msg):
    if "as an officer" in msg.lower():
        if user.upper() == TheShip.Commander.upper():
            self.msg(channel,"Yes, sir.")
            officers.append(msg.split(" ")[-4])
    elif "an officer" in msg.lower() and "is" in msg.lower():
        if msg.split(" ")[-3] in officers:
            self.msg(channel,"Yes, that person is an officer of this ship.")


def whereami(self, user, channel, msg):
    if TheShip.Docked:
        self.msg(channel,"We are currently docked at "+TheShip.Location.Name)
    else:
        self.msg(channel,"We are currently at "+TheShip.Location.Name)

def planetScan(self, user, channel, msg):
        self.msg(channel,"Planetary Surveilance Module results:")
        self.msg(channel,"Name: " + TheShip.Location.Name)
        self.msg(channel,"Mass: " + TheShip.Location.Mass() + " | Inhabited: " + TheShip.Location.Inhabited + " | Atmosphere: " +  TheShip.Location.Atmosphere)
        self.msg(channel,"Fuel to Orbit Requirement: " + TheShip.FuelNeededToLaunch())

def launchseq(self, user, channel, msg):
    if user in officers or user == TheShip.Commander:
        self.msg(channel,"Yes, sir. Running launch sequence.")

        TheShip.LaunchReady = True

        if not TheShip.Engines:
            self.msg(channel,"The engines are not operating.")
            TheShip.LaunchReady = False

        if TheShip.FuelAmount < TheShip.FuelNeededToLaunch():
            self.msg(channel,"We do not have enough fuel to get into orbit.")
            TheShip.LaunchReady = False

        if TheShip.Docked:
            self.msg(channel,"The ship is still docked.")
            TheShip.LaunchReady = False

        if TheShip.LaunchReady:
            self.msg(channel,"Sequence succeeded. The ship is ready to launch.")
    else:
        self.msg(channel,"Only the Commander or an officer may issue this command.")


def launch(self, user, channel, msg, reg_groups):
    if user == TheShip.Commander:
        if TheShip.LaunchReady:
            self.msg(channel,"Yes, sir. Commencing burn into orbit.")
            TheShip.FuelAmount -= TheShip.FuelNeededToLaunch()
            TheShip.Orbiting = True
        else:
            self.msg(channel,"The ship is not ready for launch, sir.")
    else:
        self.msg(channel,"Only the Commandermay issue this command.")


def dockoff(self, user, channel, msg):
    if user in officers or user == TheShip.Commander:
        self.msg(channel,"Disengaging from dock.")
        if random.randint(0,1000) > 10:
            self.msg(channel,"Starboard latches clear.")
        else:
            self.msg(channel,"Starboard-side latches are jammed, sir.")
            return
        if random.randint(0,1000) > 10:
            self.msg(channel,"Port latches clear.")
            return
        else:
            self.msg(channel,"Port-side latches are jammed, sir.")
        TheShip.Docked = False
        self.msg(channel,"TheShip now fully disengaged from the dock, sir.")
    else:
        self.msg(channel,"Only the Commander or an officer may issue this command.")


def promote(self, user, channel, msg, reg_groups):
    if user in officers or user == TheShip.Commander:
        if not reg_groups[0] in officers:
            self.msg(channel, "Yes, sir")
            officers.append(reg_groups[0])
            self.msg(channel, reg_groups[0] + " has been promoted.")



commands["you are dismissed"] = dismissed
commands["who are you"] = whoami
commands["what are you"] = whoami
commands["ship status"] = shipstat
commands["ship's status"] = shipstat
commands["engines"] = engines
commands["an officer"] = crew
commands["where are"] = whereami
commands["prepare to launch"] = launchseq
commands["prep to launch"] = launchseq
commands["undock"] = dockoff
commands["disengage from dock"] = dockoff
commands["planetscan"] = planetScan

complex_commands["make (.*) an officer"] = promote
complex_commands["(?=.*\b(put|launch)\b)(?=.*\b(into|in)\b)(?=.*\b(orbit)\b)^.*$"] = launch

class MessageLogger:
    """
    An independent logger class (because separation of application
    and protocol logic is a good thing).
    """
    def __init__(self, file):
        self.file = file

    def log(self, message):
        """Write a message to the file."""
        timestamp = time.strftime("[%H:%M:%S]", time.localtime(time.time()))
        self.file.write('%s %s\n' % (timestamp, message))
        self.file.flush()

    def close(self):
        self.file.close()


class LogBot(irc.IRCClient):
    """A logging IRC bot."""
    
    nickname = "SpaceShip"
    
    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        self.logger = MessageLogger(open(self.factory.filename, "a"))
        self.logger.log("[connected at %s]" % 
                        time.asctime(time.localtime(time.time())))

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        self.logger.log("[disconnected at %s]" % 
                        time.asctime(time.localtime(time.time())))
        self.logger.close()


    # callbacks for events

    def signedOn(self):
        """Called when bot has succesfully signed on to server."""
        self.join(self.factory.channel)

    def joined(self, channel):
        """This will get called when the bot joins the channel."""
        self.logger.log("[I have joined %s]" % channel)

    def privmsg(self, user, channel, msg):
        """This will get called when the bot receives a message."""
        user = user.split('!', 1)[0]
        self.logger.log("<%s> %s" % (user, msg))
        
        # Check to see if they're sending me a private message
        if channel == self.nickname:
            msg = "It isn't nice to whisper!  Play nice with the group."
            self.msg(user, msg)
            return

        # Otherwise check to see if it is a message directed at me
        if msg.startswith(self.nickname + ":") or msg.startswith(self.nickname + ","):
            #msg = "%s: I am a log bot" % user
            #self.msg(channel, msg)
            res = None
            for cc in complex_commands:
                    res = re.search(cc, msg)
            if res:
                complex_commands[cc](self, user, channel, msg, res.groups())
            else:
                for i in commands:
                    if i.upper() in msg.upper():
                        commands[i](self, user, channel, msg)

            #elif "you are dismissed".upper() in msg.upper():
                #reactor.stop()
            self.logger.log("<%s> %s" % (self.nickname, msg))

    def action(self, user, channel, msg):
        """This will get called when the bot sees someone do an action."""
        user = user.split('!', 1)[0]
        self.logger.log("* %s %s" % (user, msg))

    # irc callbacks

    def irc_NICK(self, prefix, params):
        """Called when an IRC user changes their nickname."""
        old_nick = prefix.split('!')[0]
        new_nick = params[0]
        self.logger.log("%s is now known as %s" % (old_nick, new_nick))


    # For fun, override the method that determines how a nickname is changed on
    # collisions. The default method appends an underscore.
    def alterCollidedNick(self, nickname):
        """
        Generate an altered version of a nickname that caused a collision in an
        effort to create an unused related name for subsequent registration.
        """
        return nickname + '^'



class LogBotFactory(protocol.ClientFactory):
    """A factory for LogBots.

    A new protocol instance will be created each time we connect to the server.
    """

    def __init__(self, channel, filename):
        self.channel = channel
        self.filename = filename

    def buildProtocol(self, addr):
        p = LogBot()
        p.factory = self
        return p

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()


if __name__ == '__main__':
    # initialize logging
    log.startLogging(sys.stdout)
    
    print sys.argv

    # create factory protocol and application
    f = LogBotFactory(sys.argv[1], sys.argv[2])

    # connect factory to this host and port
    reactor.connectTCP("10.8.0.38", 6667, f)

    # run bot
    reactor.run()
