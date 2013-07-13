#!/usr/bin/env python
import sys,os
from datetime import *
#----------------Use Django Mysql model----------------
import db_connector

#----------------Use Paramiko to connect ssh-----------
import paramiko
import logger
import MultiRunCounter

try:
	if sys.argv[1] == '-h':
		print '''
usage:    runSFTP.py ip user option localfile remote_path -t track_mark --single 
-s   :    send file , e.g: ./runSFTP.py 192.168.2.13 alex -s local_filename.tgz /remoteServerPath/ -t 355
		     ./runSFTP.py 192.168.2.13 alex -s local_filename.tgz /remoteServerPath/ --single
-g   :    get file,   e.g: ./demo3_sftp.py 192.168.91.171 alex -g /remotePath/Remote_filename.tgz -t 365
		     ./demo3_sftp.py 192.168.91.171 alex -g /remotePath/Remote_filename.tgz --single

--single: run in single mode,it will create a trackmark in DB automatically.
-t track_mark: set the trackmark for this file transfer operation,usually use in multi-process mode
'''
		sys.exit()
except IndexError:
	print "invalid argument followed after the script, try -h for help."
	sys.exit()
try:
	if '-t' in sys.argv:
		track_mark_index = sys.argv.index('-t') + 1
		track_mark = int(sys.argv[track_mark_index]) 
	else:
        	add_track_mark = MultiRunCounter.AddNumber()
        	track_mark = int(add_track_mark)	
except ValueError:
	print "wrong track_mark provided after -t, expect a int type by get str"
if '--single' in sys.argv:
	multi_run = 0
else:
	multi_run = 1	


Split_line="------------- "
home = os.environ['HOME']
h=db_connector.IpMachine.objects.get(ip = sys.argv[1])
host= h.ip 
port= int(h.port )
user_description = sys.argv[2] 
username = db_connector.RemoteUser.objects.get(description= user_description).user_name
password = db_connector.RemoteUser.objects.get(description= user_description).password
option = sys.argv[3]
try:
	run_user = sys.argv[6]
except IndexError:
	run_user = 'TestSftpUser'

s = paramiko.SSHClient()
s.load_system_host_keys()
s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
	t = paramiko.Transport((host,port))

	if h.protocol_type.protocol == 'SSH_KEY':
		pkey_file = '/home/alex/.ssh/id_rsa'
		key = paramiko.RSAKey.from_private_key_file(pkey_file)
		t.connect(username=username,pkey=key)
	elif h.protocol_type.protocol == 'SSH':
		t.connect(username=username,password=password)

except paramiko.AuthenticationException:
	msg= host,'---Authentication failed!'
	print msg
	logger.RecordLog(host,'SftpConnection','N/A',msg,'Error',track_mark,run_user,multi_run)
	sys.exit()
except paramiko.SSHException:
	msg= host,'---Unable to connect,no route to host!'
	print msg
	logger.RecordLog(host,'SftpConnection','N/A',msg,'Error',track_mark,run_user,multi_run)
	sys.exit()
#except :
#	msg =  host,'---timeout '
#	print msg
#	logger.RecordLog(host,'SftpConnection','N/A',msg,'Error',track_mark,run_user)
#	sys.exit()


sftp = paramiko.SFTPClient.from_transport(t)
remote_path = sys.argv[5] 
triaquae_dir = '/tmp'
if option == '-s': #send file
	local_file = sys.argv[4]
	filename = local_file.split('/')[-1]
	remote_file ='%s/%s' %(remote_path,filename)
	msg= '------- sending file %s to %s -------' %(local_file,host)
	print msg
	try:
		sftp.mkdir(remote_path)
	except IOError:pass
	sftp.put(local_file,remote_file)
		
	msg = host,"send file %s to remote directory successful: %s, under %s's home direcotry" % (filename,remote_path,username)
	logger.RecordLog(host,'SendFile','N/A',msg,'Success',track_mark,run_user,multi_run)
	sftp.put(local_file,remote_file)
	print 'Done!'
elif option == '-g': # get file
	try:
        	os.mkdir('%s/%s' %(triaquae_dir,remote_path))
	except OSError:
        	pass
	remote_file = sys.argv[4]
	filename = remote_file.split('/')[-1]
	local_file = '%s/%s_%s' %(triaquae_dir,host,filename)
	print '------- getting file %s from %s -------' %(remote_file,host)
	try:
		sftp.lstat(remote_file)	
		sftp.get(remote_file,local_file)
		print 'put file %s into local path: ' % local_file
		msg = "Result:",'Get file %s from remote ip %s and put it into local path: %s successful' %(remote_file,host,local_file)
		logger.RecordLog(host,'GetFile','N/A',msg,'Success',track_mark,run_user,multi_run)
		print 'Done'	
	except IOError:
		msg= 'Error:','file on remote ip %s not exist or it is a directory!' % host
		print msg
		logger.RecordLog(host,'GetFile','N/A',msg,'Error',track_mark,run_user,multi_run)

	
'''
try:
	sftp.put(localfile,'/root/demo3_sftp.py')
except IOError:
	print 'File path not exist or permission denied on remote server,put the file in default path /tmp'
	sftp.mkdir('TriAquae_sftp')
	sftp.put(localfile,'TriAquae_sftp/demo3_sftp.py22')
#chan = s.invoke_shell()
#interactive.interactive_shell(chan)
#chan.close()


#stdin,stdout,stderr = s.exec_command(cmd)
'''
s.close()
