#!/usr/bin/python
from subprocess import Popen,PIPE
import time

time.sleep(10)

ip_list = ['192.168.60.34','192.168.134.137','192.168.134.1']
status_dic = {}

for ip in ip_list:
	p = Popen(['ping','-c','3',ip],stdout = PIPE)
	status_dic[ip] = [p.communicate()]
	#p.communicate()
	
print status_dic
