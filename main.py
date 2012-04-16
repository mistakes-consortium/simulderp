import irc

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
        else:
            self.say(channel, "Unimplemented")

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

irc.start_reactor(SimulderpInterface, "irc.someserver.net", 6667, "#mc")
