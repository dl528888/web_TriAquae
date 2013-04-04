from django.shortcuts import render_to_response
from django.http import HttpResponse
from triWeb.models import IP

FileName = '/usr/local/TriAquae2.1.0/conf/server_list/Group_New_server'

def addServer(request):
	f = file(FileName)
	ip_list = []
	while True:
		line = f.readline()
		if len(line) == 0:break
		line2 = line.split()
		ip_address = line2[0]
		user_name = line2[1]
		user_password = line2[2]
		serverName = 'server_%s' %ip_address
		IP.objects.create(ip=ip_address,username=user_name,password=user_password,server_name=serverName,opreating_system='Redhat As 6',status='UP',agent='NO',creater_id='1')
		ip_list.append(ip_address)	
	return render_to_response('addManyServers.html',{'ip_list':ip_list})





