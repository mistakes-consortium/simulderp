#!/usr/bin/env python
import irc
import sys
import simulproto

class SimulderpInterface(irc.IRCInterface):
    started = False
    filename = None
    in_nicks = []
    ready_nicks = []

    def COMMAND_HELP(self, nick, channel, args):
        self.say(channel, "simulderp (c) 2012 mistakes consortium")
        self.say(channel, "https://github.com/mistakes-consortium/simulderp")

    def COMMAND_START(self, nick, channel, args):
        if self.started == True:
            self.say(channel, "Simulwatch already started with file "+self.filename)
        else:
            try:
                filename = args.pop()
            except IndexError:
                self.say(channel, ">start needs a filename")
                return
            self.say(channel, "Starting simulwatch of "+filename)
            self.started = True
            self.filename = filename

    def COMMAND_STOP(self, nick, channel, args):
        if self.started != True:
            self.say(channel, "No simulwatch started")
        else:
            self.started = False
            self.filename = None
            self.in_nicks = []
            self.ready_nicks = []
            self.say(channel, "Simulwatch stopped")

    def COMMAND_IMIN(self, nick, channel, args):
        if self.started != True:
            self.say(channel, "No simulwatch started")
        elif nick in self.in_nicks:
            self.say(channel, "You're already in")
        else:
            self.in_nicks.append(nick)
            self.say(channel, nick+" is in!")

    def COMMAND_READY(self, nick, channel, args):
        if self.started != True:
            self.say(channel, "No simulwatch started")
        elif nick in self.ready_nicks:
            self.say(channel, "You're already ready")
        elif not nick in self.in_nicks:
            self.say(channel, "You're not in!")
        else:
            self.ready_nicks.append(nick)
            self.say(channel, nick+" is ready!")

    def COMMAND_COUNT(self, nick, channel, args):
        if self.started != True:
            self.say(channel, "No simulwatch started")
        elif self.in_nicks != self.ready_nicks:
            not_ready_nicks = list(set(self.in_nicks)-set(self.ready_nicks))
            if len(not_ready_nicks)>1:
                self.say(channel, ', '.join(not_ready_nicks[:-1])+" and "+ not_ready_nicks[-1] +" are not ready yet :(")
            else:
                self.say(channel, not_ready_nicks[0] + " is not ready yet :(")
        elif self.in_nicks == [] :
            self.say(channel, "Nobody is in.")
        else:
            self.say(channel, "Everyone is ready!")
        self.say_unicode(channel, "incidentally, %s are connected via simulslave." % ', '.join(self.factory.simulmaster.all_slaves))

    def COMMAND_BRB(self, nick, channel, args):
        if self.started != True:
            self.say(channel, "No simulwatch started")
        else:
            self.say(channel, nick+" will brb")
            try:
                self.in_nicks.remove(nick)
            except: pass
            try:
                self.ready_nicks.remove(nick)
            except: pass

try :
    serv = sys.argv[1]
    port = 6667
    nick = sys.argv[2]
    chan = sys.argv[3]

    cmd_url = sys.argv[4]
    adv_url = sys.argv[5]

except IndexError :
    sys.stderr.write('usage: ./simulmaster.py <server> <nick> <channel> <cmd_url> <adv_url>\n')
    sys.exit(1)

simulmaster = simulproto.Master(cmd_url, adv_url)
simulmaster.start()
irc.start_reactor(SimulderpInterface, serv, 6667, nick, chan, simulmaster)
