#!/usr/bin/env python
import db_connector
from web01.models import AuthMethod,IpMachine,IpGroup
'''log_item = HostLog.objects.create(
		ip = Host,
		event_type = LogType,
		cmd = Cmd,
		event_log = Log,
		result = Result,			
		note = Note,
		track_mark = trace_num,
		user = run_user
	)
'''
g_name = IpGroup.objects.get(group_name ='Shanghai')
auth = AuthMethod.objects.get(protocol = 'SSH')

for i in range(1,254):
	addr = '192.168.2.%s' % i
	add_server = IpMachine.objects.create(

	ip = addr, 
	host_name = addr,
	protocol_type= auth,
	port = 22,
	opreating_system =  'Linux test',
	#group = g_name,

	)	

	add_server.group.add(g_name)


