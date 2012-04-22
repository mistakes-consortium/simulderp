import time
import zmqsub

class Simul(object) :
	def __init__(self, cmd_url, adv_url) :
		self.cmd_url = cmd_url
		self.adv_url = adv_url

	def step(self, max_io=1.0) :
		now = time.time()
		deadline = now + max_io
		while True :
			try :
				msg = self.ins.recv(timeout=max(0.0, deadline-now))
				
				mtype = msg['mtype']
				handler = 'handle_%s' % mtype
				if hasattr(self, handler) :
					getattr(self, handler)(msg)
				else :
					print 'ignored unknown mtype %s' % mtype

				now = time.time()
			except zmqsub.NoMessagesException :
				break

		self.step_end()

	def step_end(self) :
		pass

class Master(Simul) :
	def __init__(self, cmd_url, adv_url) :
		Simul.__init__(self, cmd_url, adv_url)
		self.outs = zmqsub.JSONZMQBindPub(self.cmd_url)
		self.ins = zmqsub.JSONZMQBindSub(self.adv_url)
		self.slaves = dict()

	def handle_slave_ready(self, msg) :
		self.slaves.setdefault(msg['src'], dict())
		self.slaves[msg['src']]['seen_ts'] = time.time()

	def handle_slave_exit(self, msg) :
		try :
			del self.slaves[msg['src']]
		except IndexError :
			pass

	def step_end(self) :
		slaves_dead = set()
		for k in self.slaves.keys() :
			if self.slaves[k]['seen_ts'] < time.time() - 10.0 :
				slaves_dead.add(k)
		for k in slaves_dead :
			del self.slaves[k]

	@property
	def all_slaves(self) :
		return self.slaves.keys()

class Slave(Simul) :
	def __init__(self, cmd_url, adv_url, nick) :
		Simul.__init__(self, cmd_url, adv_url)
		self.nick = nick
		self.ins = zmqsub.JSONZMQConnectSub(self.cmd_url)
		self.outs = zmqsub.JSONZMQConnectPub(self.adv_url)

		self.announced_file = 0.0
		self.announced_self = 0.0

	def step_end(self) :
		if time.time() > self.announced_self + 5.0 :
			self.announced_self = time.time()
			self.outs.send({
				'mtype' : 'slave_ready',
				'src' : self.nick
			})
