import sys,os
from datetime import *
sys.path.append('/home/alex/Django-1.5/django/bin/mysite')
os.environ['DJANGO_SETTINGS_MODULE'] ='mysite.settings'
#----------------Use Django Mysql model----------------
from mysite import settings

from  triWeb.models  import IP,Group

#----------------Use Paramiko to connect ssh-----------
import paramiko
import logger
#print sys.argv

Split_line="------------- "
home = os.environ['HOME']
h=IP.objects.get(ip = sys.argv[1])
host= h.ip 
port= int(h.port )
username = h.username 
password = h.password
option = sys.argv[2]
try:
	track_mark = sys.argv[4]
except IndexError:
	track_mark = 0
try:
	run_user = sys.argv[5]
except IndexError:
	run_user = 'TestSftpUser'

s = paramiko.SSHClient()
s.load_system_host_keys()
s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
	t = paramiko.Transport((host,port))

	if h.protocol_type.protocol == 'SSH_key':
		pkey_file = '/home/alex/.ssh/id_rsa'
		key = paramiko.RSAKey.from_private_key_file(pkey_file)
		t.connect(username=username,pkey=key)
	elif h.protocol_type.protocol == 'SSH':
		t.connect(username=username,password=password)

except paramiko.AuthenticationException:
	msg= host,'---Authentication failed!'
	print msg
	logger.RecordLog(host,'SftpConnection','N/A',msg,'Error',track_mark,run_user)
	sys.exit()
except paramiko.SSHException:
	msg= host,'---Unable to connect,no route to host!'
	print msg
	logger.RecordLog(host,'SftpConnection','N/A',msg,'Error',track_mark,run_user)
	sys.exit()
except :
	msg =  host,'---timeout '
	print msg
	logger.RecordLog(host,'SftpConnection','N/A',msg,'Error',track_mark,run_user)
	sys.exit()


sftp = paramiko.SFTPClient.from_transport(t)
sftp_dir = 'TriAquae_sftp'
triaquae_dir = '/tmp'
if option == '-s': #send file
	local_file = sys.argv[3]
	filename = local_file.split('/')[-1]
	remote_file ='%s/%s' %(sftp_dir,filename)
	msg= '------- sending file %s to %s -------' %(local_file,host)
	print msg
	try:
		sftp.mkdir(sftp_dir)
	except IOError:pass
	sftp.put(local_file,remote_file)
		
	msg = host,"send file %s to remote directory successful: %s, under %s's home direcotry" % (filename,sftp_dir,username)
	logger.RecordLog(host,'SendFile','N/A',msg,'Success',track_mark,run_user)
	sftp.put(local_file,remote_file)
	print 'Done!'
elif option == '-g': # get file
	try:
        	os.mkdir('%s/%s' %(triaquae_dir,sftp_dir))
	except OSError:
        	pass
	remote_file = sys.argv[3]
	filename = sys.argv[3].split('/')[-1]
	local_file = '%s/%s/%s_%s' %(triaquae_dir,sftp_dir,host,filename)
	print '------- getting file %s from %s -------' %(remote_file,host)
	try:
		sftp.lstat(remote_file)	
		sftp.get(remote_file,local_file)
		print 'put file %s into local path: ' % local_file
		msg = "Result:",'Get file %s from remote ip %s and put it into local path: %s successful' %(remote_file,host,local_file)
		logger.RecordLog(host,'GetFile','N/A',msg,'Success',track_mark,run_user)
		print 'Done'	
	except IOError:
		msg= 'Error:','file on remote ip %s not exist or it is a directory!' % host
		print msg
		logger.RecordLog(host,'GetFile','N/A',msg,'Error',track_mark,run_user)

	
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
