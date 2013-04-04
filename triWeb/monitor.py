from django.shortcuts import render_to_response
from triWeb.models import IP

def server_status(request):
	ip_pool = IP.objects.values()
	ip_dic = [] 
	for item in ip_pool:
		item['ip'] = '177.23.4.3'
		item.save()
	
	return render_to_response('status.html',{'ip':ip_dic} )
