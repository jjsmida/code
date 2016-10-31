#!/usr/bin/env python
#coding:utf8
"""
use nmap to scan critical-services
python redis_scan.py -h ip_file
"""
import os
import sys
import getopt
import re
import time
import threading

services = 'redis|mysql|oracle|memcache|mongodb|ms\-sql|http|ssh|telnet|docker|radmin|vnc|ftpd|ms\-wbt|ms\-term|rsync|nfs|rpcbind|zabbix|netbios\-ssn|microsoft\-ds'
result_files = 'results'
def mthread(ip):
	print 'Start scan',ip
	start = time.clock()
	cmd = 'nmap -sV -p1-65535 ' + ip
	foutput = os.popen(cmd)
	result = foutput.read()
	
	try:
		os.mkdir(result_files)
	except Exception,e:
		pass
	if not os.path.exists(result_files):
		print 'error, path',result_files,'donnot exists'
		sys.exit()
	#save all	
	output = open(result_files+'/'+ip+'_total', 'w')
	output.write(result)
	output.close()
	#no greedy
	#result = re.sub(r'1\sservice\sunrecognized.*?Service\sInfo', '', result, flags=re.S)
	#result = re.sub(r'services\sunrecognized.*?Service\sInfo', '', result, flags=re.S)

	result = re.sub(r'^SF.*', '', result, flags=re.M)

	cmd = 'echo "'+result+'" | egrep -i "Nmap\sscan\sreport|'+services+'"'
	foutput = os.popen(cmd)
	result = foutput.read()

	#open
	cmd = 'echo "'+result+'" | egrep -i "Nmap\sscan\sreport|open"'
	foutput = os.popen(cmd)
	result = foutput.read()

	#save some
	output = open(result_files+'/'+ip+'_s', 'w')
	output.write(result)
	output.close()

	end = time.clock()
	print 'Scan ',ip,'Used:',end - start

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
	print 'Use nmap to scan these ',services
	print 'Total: ',len(threads),iptoscan
	print 'Save result to dir',result_files
	


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
