#!/usr/bin/env python
#coding:utf8
"""
get network-using-app
python android_net.py
"""
import os
import sys
import platform

def main():
	_tmpfile = 'tmptmptmp'
	_result = 'android_net_result'

	system_win = platform.system()
	if system_win == "Windows":
		system_win = True

	cmd = 'adb devices'
	foutput = os.popen(cmd)
	#\tdevice
	if foutput.read().find('	device') == -1:
		print 'device error'
		sys.exit()

	cmd = 'adb shell netstat | find "tcp"'
	if not system_win:
		cmd = 'adb shell netstat | grep tcp'
	foutput = os.popen(cmd)
	output = open(_tmpfile, 'w')
	output.write(foutput.read())
	output.close()
	
	f = open(_tmpfile)
	r = open(_result, 'w')

	while 1:
		host = f.readline().strip()
		if not host:
			break

		info =  host.split()
		port = hex(int(info[3][info[3].rfind(':')+1:]))
		port = port[2:]
		cmd = 'adb shell grep -i '+ port +' /proc/net/tcp6'
		if info[0] == 'tcp':
			cmd = 'adb shell grep -i '+ port +' /proc/net/tcp'
		foutput = os.popen(cmd)
		tmpout = foutput.read()
		if not tmpout:
			continue
		
		uid = tmpout.split()[7][2:]
		if not uid:
			r.write(host + "\n")
			print host
			continue
		#change 066 to 66
		uid = str(int(uid))
		cmd = 'adb shell ps | find "u0_a'+ uid +'"'
		if not system_win:
			cmd = 'adb shell ps | grep u0_a' + uid
		foutput = os.popen(cmd)
		tmpout = foutput.read()
		tmpout = tmpout.split()
		tmpout1 = ''
		for x in tmpout:
			if x.find('.') != -1:
				tmpout1 += x+'#'
		tmpout = tmpout1.rstrip('#')
		host = host +' u0_a'+uid +' '+ tmpout
		print host
		r.write(host + "\n\n")

	f.close()
	r.close()
	os.remove(_tmpfile)


if __name__ == '__main__':

	main()
