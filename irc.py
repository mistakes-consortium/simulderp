from twisted.words.protocols import irc
from twisted.internet import reactor, protocol

class IRCInterface(irc.IRCClient):
    realname = "simulderp (c) 2012 mistakes consortium"

    @property
    def nickname(self) :
        return self.factory.nick

    def signedOn(self):
        IRCInterface.instance = self
        self.join(self.factory.channel)
        self.say(self.factory.channel, "simulderp engaged")

    def privmsg(self, user, channel, message):
        if message.startswith(">"):
            tokens = message[1:].split(' ')
            if not tokens:
                return
            command, args = tokens[0], tokens[1:]
            callback = getattr(self, "COMMAND_%s" % command.upper(), None)
            if callback:
                nick = user.split('!')[0]
                callback(nick, channel, args)

    def say_unicode(self, channel, msg) :
        self.say(channel, msg.encode('ascii', 'ignore'))

class IRCInterfaceFactory(protocol.ReconnectingClientFactory):
    def __init__(self, nick, channel, simulmaster):
        self.nick = nick
        self.channel = channel
	self.simulmaster = simulmaster

def start_reactor(protocol, host, port, nick, channel, simulmaster):
    factory = IRCInterfaceFactory(nick, channel, simulmaster)
    factory.protocol = protocol
    reactor.connectTCP(host, port, factory)
    reactor.run()
