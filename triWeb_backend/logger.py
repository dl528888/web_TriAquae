#!/usr/bin/env python


#WorkDir = "/usr/local/TriAquae2.1.0" 
import time,sys,os
import db_connector
from web01.models import OpsLogTemp,HostLog,OpsLog 
import datetime
cur_dir = os.path.dirname(os.path.abspath(__file__))
date =time.strftime('%Y_%m_%d %H:%M:%S')
	
def op_log(log_name,log):
	f=file(log_name,'a')
	date=time.strftime('%Y_%m_%d %H:%M:%S')
	record = '%s   %s\n' %(date,log)
	f.write(record)
	f.flush()
	f.close()

def RecordLogSummary(Action,LogType,TrackMark,RunUser='null',Cmd='null',TotalTasks= 0,Note='Null'):
	if Action == 'UPDATE':
		log_item = OpsLog.objects.get(track_mark = TrackMark)
		log_item.success_num = len(OpsLogTemp.objects.filter(track_mark = TrackMark,result='Success')) 
		log_item.failed_num = len(OpsLogTemp.objects.filter(track_mark = TrackMark,result='Error'))
		log_item.save()
	
	if Action == 'CREATE':
		log_item = OpsLog.objects.create(
		log_type = LogType,
		tri_user = 'BatchExctution',
		run_user = RunUser,
		cmd 	= Cmd,
		total_task = TotalTasks,
		success_num = 0,
		failed_num = 0,
		track_mark = TrackMark,

		)
	
def RecordLog(Host,LogType,Cmd,Log,Result,trace_num,run_user,multi_run,Note='Null'):
	def transfer_log_format(Log_content):
		if len(Log_content) >1:
			return "%s  %s" % (Log_content[0],Log_content[1])
		else:
			return "%s" % Log_content[0]
	log_item = OpsLogTemp.objects.create(
		ip = Host,
		event_type = LogType,
		cmd = Cmd,
		event_log = Log,
		result = Result,			
		note = Note,
		track_mark = trace_num,
		user = run_user
	)
	if multi_run == 1:
		RecordLogSummary('UPDATE',LogType,trace_num)	
	else:
		RecordLogSummary('CREATE',LogType,trace_num,run_user,Cmd,1)
		RecordLogSummary('UPDATE',LogType,trace_num)
	#msg = "%s  %s Command:'%s' %s \tTrack_mark:%s  \n%s   " % (Host,run_user,Cmd,Result,trace_num,transfer_log_format(Log))	
	#op_log("%s/track_run_num_%s.log" % (cur_dir,trace_num) , msg)

#RecordLogSummary('CREATE','BatchRun','root','df -h',20,10,2,123,'/tmp/ops_log_123.log')
#Example
#RecordLog('192.168.2.140','CommandExcution','uname -a','Excution Result....','Success',80,'RunUser')

