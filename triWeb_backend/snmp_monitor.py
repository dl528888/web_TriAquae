#!/usr/bin/env python
import os

snmp_oid_list = {
		'SystemVersion': '.1.3.6.1.2.1.1.1.0',
		#'RunningProcessNum' : '.1.3.6.1.2.1.25.4.2.1.2|wc -l',
		'EthernetName' : '1.3.6.1.2.1.31.1.1.1.1.2',
		'MainIpAddress': ".1.3.6.1.2.1.4.20|grep IpAddress|grep -v '127.0.0.1'",
		'TotalRAM' : '.1.3.6.1.2.1.25.2.2', # in KB
		'TotalSWAP': '.1.3.6.1.4.1.2021.4.3.0', # in KB
		'TotalSharedMEM': '.1.3.6.1.4.1.2021.4.15.0',  # in KB
		'TotalDiskSize' : '.1.3.6.1.4.1.2021.9.1.6.1', #in KB\
		'UsedSpace' : '.1.3.6.1.4.1.2021.9.1.9.1', # in percentage
		'PartitionName' : '.1.3.6.1.4.1.2021.9.1.3.1', #string
		'1MinLoad' : '.1.3.6.1.4.1.2021.10.1.3.1', 
		'5MinLoad' : '.1.3.6.1.4.1.2021.10.1.3.2',
		'15MinLoad' : '.1.3.6.1.4.1.2021.10.1.3.3', 
		'CpuIdle' : '.1.3.6.1.4.1.2021.11.11.0', # in percentage
	
	}

snmp_version = '2c'
community_name = 'public'

snmp_data = {}
for name,oid in snmp_oid_list.items():
	#print name,oid
	cmd = "snmpwalk -v %s -c %s %s %s" %  (snmp_version, community_name, 'localhost' , oid)
	cmd_result = os.popen(cmd).read()
	result = cmd_result.strip('\n').split('=')
	snmp_data[name] = result[1:]


for name,data in  snmp_data.items():
	if name == ''data[0].split()[1]
