from django.http import HttpResponse
from django.shortcuts import render_to_response

def ua1(request):
	try:
		ua = request.META['HTTP_USER_AGENT']
	except KeyError:
		ua = 'unkown'
	return HttpResponse("your browser is %s" %ua)

def ua2(request):
	ua = request.META.get('HTTP_USER_AGENT','unkown')
	return HttpResponse('<html><body bgcolor="#E6E6FA"><h3 style="background-color:green">Your browser is %s</h3></body><html>' % ua)

def display_meta(request):
	values = request.META.items()
	values.sort()
	
	return render_to_response('display_meta.html',{'values':values})
	#html = []
	#for k,v in values:
	#	html.append('<tr><tbody color="white" bgcolor="green"><td>%s</td><td>%s</td></tr></tbody>' %(k,v))
	#return  HttpResponse('<table >%s</table>' % '\n'.join(html))
