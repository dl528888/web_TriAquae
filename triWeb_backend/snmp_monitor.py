#!/usr/bin/env python
import os
import time 

date =time.strftime('%Y_%m_%d %H\:%M\:%S')
snmp_oid_list = {
		#'SystemVersion': '.1.3.6.1.2.1.1.1.0',
		#'RunningProcessNum' : '.1.3.6.1.2.1.25.4.2.1.2|wc -l',
		#'EthernetName' : '1.3.6.1.2.1.31.1.1.1.1.2',
		#'MainIpAddress': ".1.3.6.1.2.1.4.20|grep IpAddress|grep -v '127.0.0.1'",
		#'TotalRAM' : '.1.3.6.1.2.1.25.2.2', # in KB
		#'TotalSWAP': '.1.3.6.1.4.1.2021.4.3.0', # in KB
		#'TotalSharedMEM': '.1.3.6.1.4.1.2021.4.15.0',  # in KB
		#'TotalDiskSize' : '.1.3.6.1.4.1.2021.9.1.6.1', #in KB\
		#'UsedSpace' : '.1.3.6.1.4.1.2021.9.1.9.1', # in percentage
		#'PartitionName' : '.1.3.6.1.4.1.2021.9.1.3.1', #string
		'StorageTable' : '''hrStorageTable|awk -F'::' '{print $2 ,"None"}' ''' , # return RAM and Disk info
		'MemTable':  '''.1.3.6.1.4.1.2021.4 |awk -F'::' '{print $2 ,"None"}' ''',
		#'1MinLoad' : '.1.3.6.1.4.1.2021.10.1.3.1', 
		#'5MinLoad' : '.1.3.6.1.4.1.2021.10.1.3.2',
		#'15MinLoad' : '.1.3.6.1.4.1.2021.10.1.3.3', 
		'Load' : ".1.3.6.1.4.1.2021.10|grep laLoad.[0-9]|awk -F: '{print $4}'|xargs echo 'load='",
		'CpuIdle' : '.1.3.6.1.4.1.2021.11', # in percentage
		'CpuUsage': '''.1.3.6.1.4.1.2021.11|grep Cpu |awk -F'::' '{print $2}' ''',	
		'IfDescr' : "ifDescr |awk -F'::' '{print $2}'",
		'IfIn'	: "ifInOctets |awk -F'::' '{print $2}' ",
		'IfOut' : "ifOutOctets |awk -F'::' '{print $2}'",
	}

snmp_version = '2c'
community_name = 'public'

snmp_data = {'Mem_list' : [],'Ip_speed' : []}
Mem_list = []
Cpu_usage = []
for name,oid in snmp_oid_list.items():
	cmd = "snmpwalk -v %s -c %s %s %s" %  (snmp_version, community_name, 'localhost' , oid)
	cmd_result = os.popen(cmd).read()
	if name == 'StorageTable' or name == 'MemTable':
		snmp_data['Mem_list'].append(cmd_result.split('\n'))
		continue
	if name == 'CpuUsage':
		snmp_data[name] = cmd_result
		continue
	if name == 'IfDescr' or name == 'IfIn' or name == 'IfOut':
		snmp_data['Ip_speed'].append(cmd_result.split('\n'))
                continue		
	result = cmd_result.strip('\n').split('=')
	snmp_data[name] = result[1:]


STEP = 2
HEARTBEAT = 600 

def draw_graph(rrdfile_name,DS,addtional=0):
	if DS == 'CpuUsage':
		os.system('''rrdtool graph /var/www/%s.png \\
		--start now-1h --title "CPU Usage" \\
		--vertical-label "Idle in percentage" \\
		--color "BACK#C3CAD1" --color "CANVAS#0a0a0a"   --color "SHADEB#9999CC" \\
		--height 200 --width 600 \\
		--slope-mode --alt-autoscale \\
		DEF:value1=%s:cpu_idle:MAX  \\
		DEF:value2=%s:cpu_system:MAX \\
		DEF:value3=%s:cpu_user:MAX \\
		AREA:value1#00ff00:"cpu_idle %s" \\
		AREA:value2#0000ff:"cpu_system %s" \\
		AREA:value3#E04000:"cpu_user %s"\\
		--alt-y-grid COMMENT:"Last update %s" ''' % (DS,rrdfile_name, rrdfile_name, rrdfile_name,cpu_idle,cpu_system,cpu_user, date)  )
	if DS == 'Ip_speed':
		eth_name = addtional
		print eth_name
		os.system('''rrdtool graph /var/www/%s.png \\
		--start now-1h --title "%s speed " \\
		--vertical-label "kb" \\
		--height 200 --width 600 \\
		--slope-mode --alt-autoscale 	\\
		DEF:value1=%s:in:MAX \\
		DEF:value2=%s:out:MAX \\
		AREA:value1#f007:"in_speed %sBit" \\
		AREA:value2#0f05:"out_speed %sBit" \\
		--alt-y-grid  \\
		COMMENT:"Last update %s" \\
		''' %(eth_name,eth_name,rrdfile_name,rrdfile_name,in_speed,out_speed ,date ))
	if DS == 'Load':
		os.system('''rrdtool graph /var/www/%s.png \\
		--start now-1h --title "System Load Average" \\
		--vertical-label "LOAD AVERAGE" \\
		--height 200 --width 600 \\
		--slope-mode --alt-autoscale \\
 		DEF:value1=%s:Load_1:MAX \\
		DEF:value2=%s:Load_5:MAX \\
		DEF:value3=%s:Load_15:MAX \\
		AREA:value1#00ff00:Load_1min \\
		LINE2:value2#0000ff:Load_5 \\
		LINE3:value3#E04000:Load_15  \\
		COMMENT:"Last update %s" --alt-y-grid  ''' % (DS,rrdfile_name,rrdfile_name,rrdfile_name,date )  )
	if DS == 'Mem_list':
		os.system('''rrdtool graph /var/www/%s.png \\
		--start now-1h --title "Memory usage" \\
		--vertical-label "MEMORY(MB)"	\\
		--height 200 --width 600 \\
		--slope-mode --alt-autoscale \\
		DEF:value1=%s:RAM_used:MAX  \\
		DEF:value2=%s:Cached:MAX \\
		DEF:value3=%s:SWAP_used:MAX \\
		AREA:value1#00ff00:"RAM_used %sM" \\
		AREA:value2#006600:"Cached %sM"\\
		LINE3:value3#E04000:"SWAP_used %sM"\\
		--alt-y-grid \\
		COMMENT:"      " \\
		COMMENT:"Last update %s" \\
		COMMENT:"Total_RAM %sM" \\
		COMMENT:"Total_SWAP %sM" \\
		''' % (DS,rrdfile_name,rrdfile_name,rrdfile_name,MEM_used,Cached_MEM,SWAP_used, date,Total_RAM,Total_SWAP  ))
for name,data in  snmp_data.items():
	rrdfile = '/var/www/%s.rrd' % name
	
	if  name == 'CpuIdle':
		cpu_idle = data[0].split()[1]
		print cpu_idle
		try:
			os.lstat(rrdfile)
		except OSError:
			os.system('''rrdtool create %s --step 50  DS:%s:GAUGE:%s:0:100  RRA:MAX:0.5:1:2880 ''' % (rrdfile,name,HEARTBEAT) ) 
		os.system("rrdtool updatev %s --template %s  N:%d" % (rrdfile,name,int(cpu_idle) )) 
		draw_graph(rrdfile,name)
	elif name == 'CpuUsage':
		cpu_dic = {}
		info_list =  data.split('\n')
		for i in info_list:
			if len(i) == 0:break
			cpu_dic[i.split()[0]] = i.split()[3]
		cpu_idle = cpu_dic['ssCpuIdle.0']
		cpu_system = cpu_dic['ssCpuSystem.0']
		cpu_user = cpu_dic['ssCpuUser.0']
		try:
                        os.lstat(rrdfile)
                except OSError:
                        os.system('''rrdtool create %s --step 50 \\
			DS:cpu_idle:GAUGE:%s:0:100 \\
			DS:cpu_system:GAUGE:%s:0:100 \\
			DS:cpu_user:GAUGE:%s:0:100 \\
			RRA:MAX:0.5:1:2880 ''' % (rrdfile,HEARTBEAT,HEARTBEAT,HEARTBEAT) )

                os.system("rrdtool updatev %s --template 'cpu_idle:cpu_system:cpu_user'  N:%s:%s:%s" % (rrdfile,int(cpu_idle), cpu_system, cpu_user ))
		draw_graph(rrdfile,name)
	elif name == 'Load':
		load_1 = data[0].split()[0]
		load_5 = data[0].split()[1]
		load_15 = data[0].split()[2]
		print load_1, load_5, load_15
		try:
                        os.lstat(rrdfile)
                except OSError:
                        os.system('''rrdtool create %s --step 50  DS:Load_1:GAUGE:%s:0:100  DS:Load_5:GAUGE:%s:0:100 DS:Load_15:GAUGE:%s:0:100  RRA:MAX:0.5:1:2880 ''' % (rrdfile,HEARTBEAT,HEARTBEAT,HEARTBEAT) )
                os.system("rrdtool updatev %s --template 'Load_1:Load_5:Load_15'  N:%s:%s:%s" % (rrdfile,load_1,load_5,load_15 ))
                draw_graph(rrdfile,name)
	elif name == 'Mem_list':
		info_dic = {}
		for i in data:
		  for item in i:
			if len(item) ==0:break
			key = item.split()[0]
			value = item.split()[3]	
			info_dic[key] = value
		
		if info_dic is not None:
			Total_RAM = int(info_dic['hrStorageSize.1']) / 1024
			Total_SWAP = int(info_dic['hrStorageSize.10']) / 1024
			Cached_MEM = int(info_dic['hrStorageSize.7']) / 1024
			Free_SWAP = int(info_dic['memAvailSwap.0']) / 1024
			Free_MEM = int(info_dic['memAvailReal.0']) /1024
			Buffer_MEM = int(info_dic['memBuffer.0']) /1024
			MEM_used = Total_RAM - Free_MEM
			SWAP_used = Total_SWAP - Free_SWAP
			SWAP_used = 520
			print Total_RAM,Total_SWAP,Cached_MEM,Free_SWAP,Free_MEM,Buffer_MEM
			print "+++++++++", MEM_used,SWAP_used,Cached_MEM
			try:
				os.lstat(rrdfile)
			except OSError:
				os.system('''rrdtool create %s --step 50 \\
				DS:RAM_used:GAUGE:%s:U:U \\
				DS:Cached:GAUGE:%s:U:U \\
				DS:SWAP_used:GAUGE:%s:U:U \\
				RRA:MAX:0.5:1:300	\\
				''' % (rrdfile,HEARTBEAT,HEARTBEAT,HEARTBEAT)  )
			os.system('''rrdtool updatev %s --template 'RAM_used:Cached:SWAP_used' N:%s:%s:%s \\
			''' % (rrdfile ,MEM_used,Cached_MEM, SWAP_used ))
			draw_graph(rrdfile,name)
	elif name == 'Ip_speed':
		ip_speed_dic = {}
		
		for i in data:
			for item in i:
				if len(item) ==0:break
				ip_speed_dic[item.split()[0]] = item.split()[3]
		for obj_name,value in ip_speed_dic.items():
	
			if obj_name.startswith('ifDescr'):
				ethernet_name = ip_speed_dic[obj_name] 
				in_speed = int(ip_speed_dic['ifInOctets.%s' % obj_name[-1]]) / 8 /1000
				out_speed = int(ip_speed_dic['ifOutOctets.%s' % obj_name[-1]]) /8 /1000
				print ethernet_name,in_speed,out_speed

				rrd_file = '/var/www/%s.rrd' % ethernet_name
				try:
                                	os.lstat(rrd_file)
                        	except OSError:
					os.system('''rrdtool create %s --step 50 \\
					DS:in:GAUGE:%s:U:U \\
					DS:out:GAUGE:%s:U:U \\
					RRA:MAX:0.5:1:300 \\
					''' %(rrd_file,HEARTBEAT,HEARTBEAT ) )
				os.system('''rrdtool updatev %s --template 'in:out' N:%s:%s ''' %(rrd_file, in_speed, out_speed) )
				print '+++++++++++-------------<<<<<<<<<<<<'
				draw_graph(rrd_file,name,ethernet_name)
		print ip_speed_dic
	else :
		pass
		#print name,data
