#!/usr/bin/env python
import sys,os
from datetime import *
#----------------Use Django Mysql model----------------

#from  triWeb.models  import IP,Group,ConnectionMethod
import db_connector
#----------------Use Paramiko to connect ssh-----------

import paramiko
import logger,MultiRunCounter
#print sys.argv

Split_line="------------- "
try:
	if sys.argv[1] == '-h':
		print '''
usage	:	runCmd.py ip	'command' remote_user  track_mark
		./runCmd.py 192.168.2.14 'df -h' alex 34
--single: 	run in single mode,it means you don't need to care about the trackmark stuff,use it when only have one IP to run, this will automatically create a new trackmark in DB
		./runCmd.py 192.168.91.171 df alex --single
		'''
		sys.exit()
except IndexError:
	print "argument error,try -h for help" 
	sys.exit()
try:
	track_mark = sys.argv[4]
	if track_mark == '--single':
		track_mark = MultiRunCounter.AddNumber()
except IndexError:
	track_mark = MultiRunCounter.AddNumber()

try:
	run_user = sys.argv[3]
except IndexError:
	run_user = "Tester_single"

if  sys.argv[-1] == '--single':
	multi_run = 0 
else:
	multi_run = 1

h=db_connector.IpMachine.objects.get(ip = sys.argv[1])
host= h.ip 
port= int(h.port )
username = run_user 
password = db_connector.RemoteUser.objects.get(user_name=username).password
#pkey_file = db_connector.RemoteUser.objects.get(user_name='root',description="test").RsaKey_file_path
pkey_file= '/home/alex/.ssh/id_rsa'
cmd = sys.argv[2]


s = paramiko.SSHClient()
s.load_system_host_keys()
s.set_missing_host_key_policy(paramiko.AutoAddPolicy())


try:
	if h.protocol_type.protocol == 'SSH_KEY':
		#pkey_file = '/home/alex/.ssh/id_rsa'
		key = paramiko.RSAKey.from_private_key_file(pkey_file)
		s.connect(host,port,username,pkey=key,timeout=5)
		stdin,stdout,stderr = s.exec_command(cmd)
		#print Split_line,h.ip,Split_line

                result = stdout.read(),stderr.read()
                logger.RecordLog(host,'CommandExcution',cmd,result,'Success',track_mark,run_user,multi_run)
		print Split_line,h.ip,Split_line,'\n',
		for line in result:
			print line,
		#print stderr.read()
	elif h.protocol_type.protocol == 'SSH':
		#try:
		s.connect(host,port,username,password,timeout=5)
        	stdin,stdout,stderr = s.exec_command(cmd)
		#print Split_line,h.ip,Split_line
        	result = stdout.read(),stderr.read()
		logger.RecordLog(host,'CommandExcution',cmd,result,'Success',track_mark,run_user,multi_run)
		print Split_line,h.ip,Split_line,'\n',stdout.read()
        	if stderr.read():print 'error happend!',stderr.read()
                for line in result:
                        print line,
except paramiko.AuthenticationException:
	result = "%s ---Authentication failed!\n" %host
	print result
	logger.RecordLog(host,'CommandExcution',cmd,result,'Error',track_mark,run_user,multi_run)
except :
	result = "%s ---timeout or configration error, please manually check the connection!\n" %host
	print result
	logger.RecordLog(host,'CommandExcution',cmd,result,'Error',track_mark,run_user,multi_run)


#chan = s.invoke_shell()
#interactive.interactive_shell(chan)
#chan.close()


#stdin,stdout,stderr = s.exec_command(cmd)

s.close()

