#!/usr/bin/env python


#WorkDir = "/usr/local/TriAquae2.1.0" 
import time,sys,os
import db_connector
from web01.models import HostLog

cur_dir = os.path.dirname(os.path.abspath(__file__))
date =time.strftime('%Y_%m_%d %H:%M:%S')
	
def op_log(log_name,log):
	f=file(log_name,'a')
	date=time.strftime('%Y_%m_%d %H:%M:%S')
	record = '%s   %s\n' %(date,log)
	f.write(record)
	f.flush()
	f.close()

def RecordLog(Host,LogType,Cmd,Log,Result,trace_num,run_user,Note='Null'):
	def transfer_log_format(Log_content):
		if len(Log_content) >1:
			return "%s  %s" % (Log_content[0],Log_content[1])
		else:
			return "%s" % Log_content[0]
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
	
	msg = "%s  %s Command:'%s' %s \tTrack_mark:%s  \n%s   " % (Host,run_user,Cmd,Result,trace_num,transfer_log_format(Log))	
	op_log("%s/track_run_num_%s.log" % (cur_dir,trace_num) , msg)


#Example
#RecordLog('192.168.2.140','CommandExcution','uname -a','Excution Result....','Success',80,'RunUser')

