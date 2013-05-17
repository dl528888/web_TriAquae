from django.shortcuts import render_to_response
from triWeb.models import Group,IP

def statusCount(serverList):
	status_list = []
	for ip in serverList:
		status_list.append(ip)	
	return status_list

def groupSummary(request):
	group_list = Group.objects.filter(parent_group__contains = "TOPGROUP")	
	server_list_dic = {}
        #server_status = []
	server_status_dic = {}
	server_status_dic2 = {}
	server_status_dic2['UP'] = IP.objects.filter(status__contains = 'UP') 
        server_status_dic2['BUSY'] = IP.objects.filter(status__contains = 'BUSY')
        server_status_dic2['DOWN'] = IP.objects.filter(status__contains = 'DOWN')
        server_status_dic2['OFFLINE'] = IP.objects.filter(status__contains = 'OFFLINE')
	
	for g_name in group_list:
		server_status = []
		
		server_status.append(len(IP.objects.filter(group_name__group_name__startswith = g_name,status = "UP")))
                server_status.append(len(IP.objects.filter(group_name__group_name__startswith = g_name,status = "BUSY")))
                server_status.append(len(IP.objects.filter(group_name__group_name__startswith = g_name,status = "DOWN")))
                server_status.append(len(IP.objects.filter(group_name__group_name__startswith = g_name,status = "OFFLINE")))
		
		server_status_dic[g_name] = server_status

		#add group name and server list to dic
		server_list_dic[g_name] = IP.objects.filter(group_name__group_name__startswith= g_name)
		
		#test = statusCount(server_list_dic[g_name])
		#for ip in server_list_dic[g_name]:
		#	server_status.append(ip.status)
	sub_group_list = Group.objects.exclude(parent_group__contains =  "TOPGROUP")
	sub_server_list_dic = {}
	for sub_group_name in sub_group_list:
		sub_server_list_dic[ sub_group_name ] = IP.objects.filter(group_name__group_name__startswith = sub_group_name )

	return render_to_response('group_summary.html',{'group_list':group_list,
				  			'server_list_dic':server_list_dic,
							'server_status_dic': server_status_dic,
							'sub_server_list_dic': sub_server_list_dic,
							'sub_groups': sub_group_list,
							'server_status_dic2': server_status_dic2,
							})

