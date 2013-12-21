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

# system imports
import time, sys

commands = {}

officers = []

class Ship:
    Engines = False #on or off
    Docked = True
    Location = "Earth"
    Commander = "lordofsraam"
    Fuel = 100 #percent


def dismissed(self, user, channel, msg):
    if user.upper() == Ship.Commander.upper():
        self.msg(channel,"Yes, sir. Have a good day, sir.")
        reactor.stop()
    else:
        self.msg(channel,"I am sorry, "+user+", but only the Commander can dismiss me.")

def whoami(self, user, channel, msg):
    self.msg(channel,"I am an AI created to make space travel in this ship easier.")
    self.msg(channel,"My commanding officer, and the captain of this ship, is "+Ship.Commander)

def shipstat(self, user, channel, msg):
    self.msg(channel,"Running diagnostics checks on the ship...")
    if Ship.Engines:
        self.msg(channel,"Engines are up and running, sir.")
    else:
        self.msg(channel,"Engines are off.")
    self.msg(channel,"Fuel charges are at %d%% percent."%Ship.Fuel)
    whereami(self, user, channel, msg)

def engines(self, user, channel, msg):
    if user in officers or user == Ship.Commander:
        if "ON" in msg.upper():
            if Ship.Engines:
                self.msg(channel, "The engines are already running, sir.")
            else:
                self.msg(channel, "Warming up the engines.")
                Ship.Engines = True
        elif "OFF" in msg.upper():
            if not Ship.Engines:
                self.msg(channel, "The engines are already off, sir.")
            else:
                self.msg(channel, "Cooling down the engines.")
                Ship.Engines = False
    else:
        self.msg(channel,"Only the Commander or an officer may issue this command.")

def crew(self, user, channel, msg):
    if "as an officer" in msg.lower():
        if user.upper() == Ship.Commander.upper():
            self.msg(channel,"Yes, sir.")
            officers.append(msg.split(" ")[-4])
    elif "an officer" in msg.lower() and "is" in msg.lower():
        if msg.split(" ")[-3] in officers:
            self.msg(channel,"Yes, that person is an officer of this ship.")

def whereami(self, user, channel, msg):
    if Ship.Docked:
        self.msg(channel,"We are currently docked at "+Ship.Location)
    else:
        self.msg(channel,"We are currently at "+Ship.Location)

def launchseq(self, user, channel, msg):
    if user in officers or user == Ship.Commander:
        self.msg(channel,"Yes, sir.")
    else:
        self.msg(channel,"Only the Commander or an officer may issue this command.")

commands["you are dismissed"] = dismissed
commands["who are you"] = whoami
commands["what are you"] = whoami
commands["ship status"] = shipstat
commands["ship's status"] = shipstat
commands["engines"] = engines
commands["an officer"] = crew
commands["where are"] = whereami
commands["prepare to launch"] = launchseq
commands["prepto launch"] = launchseq

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
            if "who is in charge".upper() in msg.upper():
                self.msg(channel,"The current commander of this ship is "+Ship.Commander)
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
    reactor.connectTCP("irc.azuru.net", 6667, f)

    # run bot
    reactor.run()
