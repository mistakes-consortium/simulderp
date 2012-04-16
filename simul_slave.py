#!/usr/bin/env python

import time
import sys
import simulproto

if __name__ == '__main__' :
	cmd_url = sys.argv[1]
	adv_url = sys.argv[2]
	nick = sys.argv[3]
	
	slave = simulproto.Slave(cmd_url, adv_url, nick)

	while True :
		slave.step()
		print 'slave *thump* %s' % time.ctime()
