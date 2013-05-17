# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
from triWeb.models import IP

def ShowIPi2(request):
	ip_pool = IP.objects.values()
	ip_dic = {}
	num = 1
	for item in ip_pool:
		ip = item['ip']
		serverName = '%s_%s' %(item['server_name'],num)
		status = item['status']
		ip_dic[serverName] =  status
		
		num += 1
	TotalServers = IP.objects.count() 
	return render_to_response('monitorPage.html',{'ip_dic':ip_dic,'TotalServers':TotalServers})
def ShowIP(request):
        ip_pool = IP.objects.values()
        '''ip_dic = {}
        num = 1
        for item in ip_pool:
                ip = item['ip']
                serverName = '%s_%s' %(item['server_name'],num)
                status = item['status']
                ip_dic[serverName] =  status

                num += 1
        TotalServers = IP.objects.count()
        return render_to_response('monitorPage.html',{'ip_dic':ip_dic,'TotalServers':TotalServers})
	'''
	TotalServers = IP.objects.count()
	return render_to_response('monitorPage.html',{'ip_pool':ip_pool,'TotalServers':TotalServers,'IP_List':IP.objects.all()})
def ajaxTest(request):
	data = []
	if 'fname' in request.GET:
		data.append(request.GET['fname'])
	else:
		data.append('No data found')
	
	return render_to_response('ajax1.html',{'response_data':data}	)

def loadCD(request):
        ip_pool = IP.objects.values()
        ip_dic = {}
        num = 1
        for item in ip_pool:
                ip = item['ip']
                serverName = '%s_%s' %(item['server_name'],num)
                status = item['status']
                ip_dic[serverName] =  status

                num += 1
        TotalServers = IP.objects.count()
        return render_to_response('ajax3.html',{'txtCDInfo':ip_dic,'TotalServers':TotalServers})
	

def search_form(request):
	return render_to_response('search_form.html')


def search2(request):
	errors= []
	if 'userInput' in request.GET:
		userInput = request.GET['userInput']
		if not userInput:
			errors.append('Enter a search term')
		elif len(userInput) >20:
			errors.append('Please enter at most 20 characters.')
		else:	
			books = Book.objects.filter(title__contains=userInput)
			return render_to_response('search_result.html',{'books':books,'query':userInput})
	
	return render_to_response('search_form.html',{'error':errors})

def displayFile(request):
	filename = '/usr/local/TriAquae2.1.0/logs/operation.log'
	#def catFile():
	f = file(filename)
	content = []
	while True:
		line = f.readline()
		if len(line) == 0:break
		content.append(line)
	f.close()
	return render_to_response('showFile.html',{'filename':content})
