#!/usr/bin/env python
import os
import time 

date =time.strftime('%Y_%m_%d %H\:%M\:%S')
snmp_oid_list = {
		'SystemVersion': '.1.3.6.1.2.1.1.1.0',
		#'RunningProcessNum' : '.1.3.6.1.2.1.25.4.2.1.2|wc -l',
		'EthernetName' : '1.3.6.1.2.1.31.1.1.1.1.2',
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
		'CpuIdle' : '.1.3.6.1.4.1.2021.11.11.0', # in percentage
	
	}

snmp_version = '2c'
community_name = 'public'

snmp_data = {'Mem_list' : []}
Mem_list = []
for name,oid in snmp_oid_list.items():
	cmd = "snmpwalk -v %s -c %s %s %s" %  (snmp_version, community_name, 'localhost' , oid)
	cmd_result = os.popen(cmd).read()
	if name == 'StorageTable' or name == 'MemTable':
		snmp_data['Mem_list'].append(cmd_result.split('\n'))
		continue
	result = cmd_result.strip('\n').split('=')
	snmp_data[name] = result[1:]


STEP = 2
HEARTBEAT = 600 

def draw_graph(rrdfile_name,DS):
	if DS == 'CpuIdle':
		os.system('''rrdtool graph /var/www/%s.png \\
		--start now-1h --title "%s Usage" \\
		--vertical-label "Idle in percentage" \\
		--color "BACK#C3CAD1" --color "CANVAS#0a0a0a"   --color "SHADEB#9999CC" \\
		--height 200 --width 600 \\
		--slope-mode --alt-autoscale \\
		DEF:value1=%s:%s:MAX  \\
		AREA:value1#00ff00:%s \\
		--alt-y-grid COMMENT:"Last update %s" ''' % (DS,DS,rrdfile_name,DS,DS, date)  )
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
		--vertical-label "MEMMORY(MB)"	\\
		--height 200 --width 600 \\
		--slope-mode --alt-autoscale \\
		DEF:value1=%s:RAM_used:MAX  \\
		DEF:value2=%s:SWAP_used:MAX \\
		DEF:value3=%s:Cached:MAX  \\
		AREA:value1#00ff00:RAM_used \\
		AREA:value2#0000ff:SWAP_used \\
		AREA:value3#E04000:Cached \\
		COMMENT:"  \n" \\
		COMMENT:"Last update %s \nTotal RAM %s M" --alt-y-grid \\
		''' % (DS,rrdfile_name,rrdfile_name,rrdfile_name,date,Total_RAM  ))

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
			print Total_RAM,Total_SWAP,Cached_MEM,Free_SWAP,Free_MEM,Buffer_MEM
			SWAP_used = 400
			print "+++++++++", MEM_used,SWAP_used,Cached_MEM
			try:
				os.lstat(rrdfile)
			except OSError:
				print '=======================run'
				os.system('''rrdtool create %s --step 50 \\
				DS:RAM_used:GAUGE:%s:U:U \\
				DS:SWAP_used:GAUGE:%s:U:U \\
				DS:Cached:GAUGE:%s:U:U \\
				RRA:MAX:0.5:1:300	\\
				''' % (rrdfile,HEARTBEAT,HEARTBEAT,HEARTBEAT)  )
			
			os.system('''rrdtool updatev %s --template 'RAM_used:SWAP_used:Cached' N:%s:%s:%s \\
			''' % (rrdfile,MEM_used,SWAP_used, Cached_MEM )) 
			draw_graph(rrdfile,name)
		#for k,v in info_dic.items():print k,v
	else :
		pass
		#print name,data
