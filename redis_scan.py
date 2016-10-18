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


def main(ip_file):
	start = time.clock()
	ips = open(ip_file)
	iptoscan = ''
	count = 0
	for ip in ips:
		ip = ip.rstrip('\n')
		if ip == '':
			continue
		count += 1
		iptoscan += ip + ' '
	print 'Total: ',count,iptoscan
	cmd = 'nmap -sV -p1-65535 ' + iptoscan
	foutput = os.popen(cmd)
	result = foutput.read()
	#save all
	output = open(ip_file+'_total', 'w')
	output.write(result)
	output.close()
	#no greedy
	result = re.sub(r'1\sservice\sunrecognized.*?Service\sInfo', '', result, flags=re.S)
	result = re.sub(r'services\sunrecognized.*?Service\sInfo', '', result, flags=re.S)

	cmd = 'echo "'+result+'" | egrep -i "Nmap\sscan\sreport|redis"'
	foutput = os.popen(cmd)
	print foutput.read()

	#save some
	output = open(ip_file+'_r', 'w')
	output.write(foutput.read())
	output.close()

	end = time.clock()
	print 'Used:',end - start


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
