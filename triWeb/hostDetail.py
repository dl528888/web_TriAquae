from django.shortcuts import render_to_response
from triWeb.models import Group,IP,HostLog

def host_detail(request):
	title_list= ['Overview','Graphs','Events','Management']
	get_data = request.GET['IP_ADDR'] 
	ip_addr = IP.objects.filter(ip__contains = get_data)[0]	
	command_result = HostLog.objects.filter(track_mark=55)[0].event_log
	command_result2 = command_result.split('\\n')
	return render_to_response('host_detail.html',
		{'title_list':title_list,
		 'IP_ADDR': ip_addr,	
		 'command_result':command_result2,
		})


def navigation(request):
	
	if request.GET['overview']:
		command_result = HostLog.objects.filter(ip='192.168.2.150')[0].result
		
		return render_to_response('navigation_overview.html',{'command_result':command_result})	
		
def graphs(request):
	return render_to_response('graph.html',{})	
