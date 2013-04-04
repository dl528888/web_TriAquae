import os,sys
import time
import subprocess
from subprocess import Popen
#------------
sys.path.append('/home/alex/Django-1.4.3/django/bin/mysite')
os.environ['DJANGO_SETTINGS_MODULE'] ='mysite.settings'
from django.core.management import setup_environ
from mysite import settings
from triWeb.models import IP
setup_environ(settings)
###################-------------------------------

ip_list = IP.objects.all()
'''
for ip in ip_list:
        print ip,ip.status
#--------------------------------------

ping_status_dic = {}
p = [] # ip -> process
for n in range(1, 100): # start ping processes
    ip = "192.168.134.%d" % n
    p.append((ip, Popen(['ping', '-c', '3', ip], stdout=subprocess.PIPE)))
    #NOTE: you could set stderr=subprocess.STDOUT to ignore stderr also
'''
ping_status_dic = {}
ping_error_list = []
p = [] # ip -> process
for i in ip_list:
	ip = "%s" % i
	p.append((ip, Popen(['ping', '-c', '3', ip], stdout=subprocess.PIPE)))

while p:
    for i, (ip, proc) in enumerate(p[:]):
        if proc.poll() is not None: # ping finished
            p.remove((ip, proc)) # this makes it O(n**2)
            #ping_status_dic[ip] = proc.communicate() # add result to dic
	    if proc.returncode != 0: #error 
		ping_error_list.append(ip)
	    else:
                ping_status_dic[ip] = proc.communicate() # add result to dic
    time.sleep(.04)


for ip,result in ping_status_dic.items():
	status = result[0].split('received,')[1].split('%')[0].strip()
	if 'rtt' in result[0]: # normal
		rtt = result[0].split('\n')[-2]
		print ip,status,rtt
		ok_ip = IP.objects.get(ip=ip)
		ok_ip.ping_status = rtt
		ok_ip.status = 'UP'
		ok_ip.save()
	elif 'error' in status:   #unreachable
		print ip,'err',status.split()[-1]

	else:   # 
		print ip,'---->packet loss',status

#--------------------------- 
# ping doesn't work ,use nc to scan port 
T = []
Port_status_dic = {}
if len(ping_error_list) > 0:
	for i in ping_error_list:
		ip = "%s" % i
        	T.append((ip, Popen(['nc', '-w', '1', ip,'22'], stdout=subprocess.PIPE)))
	
	while T:
		for i, (ip,proc) in enumerate(T[:]):
			if proc.poll() is not None:
				T.remove((ip,proc))
				if proc.returncode == 0:
					Port_status_dic[ip] = 'YES'
				else:
					Port_status_dic[ip] = 'NO'
	time.sleep(.04)

	if Port_status_dic:
		for err_ip,port_status in Port_status_dic.items():
			print err_ip,port_status
			ip = IP.objects.get(ip=err_ip)
			msg= "Ping doesn't work. Telnet port:22 Reachable: %s" % port_status
			ip.ping_status = msg
			if port_status == 'NO':
				ip.status = 'DOWN'
			ip.save()
