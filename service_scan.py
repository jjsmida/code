#!/usr/bin/env python
#coding:utf8
"""
use nmap to scan redis-server
python redis_scan.py -h ip_file
"""
import os
import sys
import getopt
import re
import time
import threading


def mthread(ip):
	print 'start scan',ip
	start = time.clock()
	cmd = 'nmap -sV -p1-65535 ' + ip
	foutput = os.popen(cmd)
	result = foutput.read()
	#save all
	output = open(ip+'_total', 'w')
	output.write(result)
	output.close()
	#no greedy
	result = re.sub(r'1\sservice\sunrecognized.*?Service\sInfo', '', result, flags=re.S)
	result = re.sub(r'services\sunrecognized.*?Service\sInfo', '', result, flags=re.S)

	cmd = 'echo "'+result+'" | egrep -i "Nmap\sscan\sreport|redis"'
	foutput = os.popen(cmd)
	result = foutput.read()

	#save some
	output = open(ip+'_s', 'w')
	output.write(result)
	output.close()

	end = time.clock()
	print 'scan ',ip,'Used:',end - start

def main(ip_file):
	
	ips = open(ip_file)
	iptoscan = ''
	threads = []
	for ip in ips:
		ip = ip.rstrip('\n')
		if ip == '':
			continue
		threads.append(threading.Thread(target=mthread,args=(ip,)))
		iptoscan += ip + ' '
	for t in threads:
		t.setDaemon(False)
		t.start()
	print 'Total: ',len(threads),iptoscan
	


if __name__ == '__main__':
	ip_file = ''
	options,args = getopt.getopt(sys.argv[1:],"h:")

	for opt,arg in options:
		if opt == '-h':
			ip_file = arg

	if not os.path.exists(ip_file) :
		#print '\033[1;31;40m'
		print 'python redis_scan.py -h ip_file'
		#print '\033[0m'
		sys.exit()


	main(ip_file)
