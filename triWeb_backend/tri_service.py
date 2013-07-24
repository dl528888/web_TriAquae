#!/usr/bin/env python

import os,sys,time
import logger
working_dir = logger.cur_dir
status_check_script = 'host_status_check.py'
def status_monitor(interval):
	script = '%s/%s' %(working_dir,status_check_script)
	print "Checking service status....."
	if service_status() == 'Running':
		print "service is already running!"
	else:
		print "Starting service...."
		cmd = 'nohup python %s -s %s > tri_service.log &' % (script,interval)
		result  = os.system(cmd)
		if result == 0:
			print 'Host status monitor service started!'

def stop_service():
	cmd = "ps -ef| grep %s|grep -v grep |awk '{print $2}'|xargs kill -9" %(status_check_script)	
	
	if service_status() == 'Running':
		cmd_result = os.system(cmd)
		if cmd_result == 0:
			print '..............\n'
			time.sleep(1)
			print 'stopped!'

	else:
		print 'Service is not running...,nothing to kill! '
def service_status():
	cmd = "ps -ef |grep %s|grep -v grep |awk '{print $2}'" % status_check_script
	result = os.popen(cmd).read().strip()
	try:
		service_pid = result.split()[0]
		if service_pid:
			print "host status monitor service is running..."
			return "Running"
	except IndexError:
		print "host status monitor service is not running...."
		return "Dead"
try:
	if sys.argv[1] == 'start':
		status_monitor(15)
	elif sys.argv[1] == 'stop':
		stop_service()
	elif sys.argv[1] == 'status':
		service_status()
except IndexError:
	
	print 'No argument detected!\nUse: stop|start|status'
