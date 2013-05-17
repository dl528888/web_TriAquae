import os
import time
import subprocess
from subprocess import Popen

devnull = open(os.devnull, 'wb')
ping_status_dic = {}
p = [] # ip -> process
for n in range(1, 100): # start ping processes
    ip = "192.168.134.%d" % n
    p.append((ip, Popen(['ping', '-c', '3', ip], stdout=subprocess.PIPE)))
    #NOTE: you could set stderr=subprocess.STDOUT to ignore stderr also

while p:
    for i, (ip, proc) in enumerate(p[:]):
        if proc.poll() is not None: # ping finished
            p.remove((ip, proc)) # this makes it O(n**2)
            if proc.returncode == 0:
                print('%s active' % ip)
		ping_status_dic[ip] = proc.communicate()
            elif proc.returncode == 2:
                print('%s no response' % ip)
                ping_status_dic[ip] = proc.communicate()
            else:
                print('%s error' % ip)
                ping_status_dic[ip] = proc.communicate()
    time.sleep(.04)
devnull.close()

for ip,result in ping_status_dic.items():
	status = result[0].split('received,')[1].split('%')[0].strip()
	if 'rtt' in result[0]:
		rtt = result[0].split('\n')[-2]
		print ip,status,rtt
	elif 'error' in status:   
		print ip,'err',status.split()[-1]
	else:
		print ip,'---->packet loss',status


