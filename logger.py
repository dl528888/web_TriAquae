#!/usr/bin/env python


#WorkDir = "/usr/local/TriAquae2.1.0" 
import time,sys
import db_connector
from triWeb.models import HostLog


op_log_file='operation.log' 
date =time.strftime('%Y_%m_%d %H:%M:%S')
	
def op_log(log):
	f=file(op_log_file,'a')
	date=time.strftime('%Y_%m_%d %H:%M:%S')
	record = '%s   %s\n' %(date,log)
	f.write(record)
	f.flush()
	f.close()
#----

def RecordLog(Host,LogType,Cmd,Log,Result,trace_num,run_user,Note='Null'):
	def transfer_log_format(Log_content):
		if len(Log_content) >1:
			return "<--\n  %s  %s-->" % (Log_content[0],Log_content[1])
		else:
			return "<--\n  %s-->" % Log_content[0]
	log_item = HostLog.objects.create(
		ip = Host,
		event_type = LogType,
		cmd = Cmd,
		event_log = Log,
		result = Result,			
		note = Note,
		track_mark = trace_num,
		user = run_user
	)
	# Also input log to log file
	
	msg = "\033[36;1m%s  %s Command:'%s' %s \tTrack_mark:%s\033[0m \n%s   " % (Host,run_user,Cmd,Result,trace_num,transfer_log_format(Log))	
	op_log(msg)


#Example
	#RecordLog('192.168.2.140','CommandExcution','uname -a','Excution Result....','Success',80,'RunUser')

