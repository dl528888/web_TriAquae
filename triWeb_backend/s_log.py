

import os,json

f= file('snmp.log')
performance_dic = {}
for i in f.readlines():
    try:
        line = i.strip().split('|')
        if line[1].strip() == 'OK':
            performance_dic[line[0]] =  json.loads(line[2])
        #print line,len(line)
    except IndexError:continue

import db_connector
mail_dic = {}

for h,dic in performance_dic.items():
    mail_dic[h] = [] #create an empty snmp data list for each host
    server = db_connector.IpMachine.objects.get(ip=h)
    print server.system_load_warning, server.system_load_critical, server.cpu_idle_warning,server.cpu_idle_critical
    print int(dic['CpuIdle'])
    
    if server.cpu_idle_critical != 0 and int(dic['CpuIdle']) - server.cpu_idle_critical <= 0:
        mail_dic[h].append('Critical: Value of CpuIdle is %s,exceeds the limit %s' %(int(dic['CpuIdle']), server.cpu_idle_critical))
    elif server.cpu_idle_warning != 0 and int(dic['CpuIdle'])  - server.cpu_idle_warning <= 0: 
        mail_dic[h].append('Warning: Value of CpuIdle is %s,exceeds the limit %s' %(int(dic['CpuIdle']), server.cpu_idle_warning))
    else: 
        print h,'not hitting the alert line yet!'
    
    
    if server.system_load_critical !=0 and float(dic['SystemLoad']) - server.system_load_critical >=0:
        mail_dic[h].append('Critical: Value of System Load is %s,exceeds the limit %s' %(float(dic['SystemLoad']), server.system_load_critical))
    elif server.system_load_warning != 0 and float(dic['SystemLoad']) - server.system_load_warning >=0:
        mail_dic[h].append('Warning: Value of System Load is %s,exceeds the limit %s' %(float(dic['SystemLoad']),server.system_load_warning))
    else:
        print h,'not hitting the SYSTEM LOAD alert line yet!'
   
    if server.mem_usage_critical != 0 and float(dic['MemUsage']) - server.mem_usage_critical  >= 0:
        mail_dic[h].append('Critical: Value of Memusage is %s,exceeds the limit %s' %(float(dic['MemUsage']),server.mem_usage_critical))
    elif server.mem_usage_warning != 0 and float(dic['MemUsage']) - server.mem_usage_warning >=0:
        mail_dic[h].append('Warning: Value of Memusage is %s,exceeds the limit %s' %(float(dic['MemUsage']),server.mem_usage_warning))
    else:
        print h,'not hitting the MEM alert line yet!'

for h,data in mail_dic.items():
    print h,data
#db_connector.IpMachine.objects.values('ip','system_load_warning','system_load_critical','cpu_idle_warning','cpu_idle_critical','mem_usage_warning','mem_usage_critical')
