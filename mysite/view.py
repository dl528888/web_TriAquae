#!/usr/bin/python
from django.http import HttpResponse
import datetime
from django.shortcuts import  render_to_response
from django.template import Context,Template
from django.template.loader import get_template
def current_datetime(request):
		now = datetime.datetime.now()
		#html = "<html><body> It is now %s.</body></html>" % now
		#return HttpResponse(html)
		#t = get_template('current_datetime.html')
		#html = t.render(Context({'current_date':now}))
		#return HttpResponse(html)
		return render_to_response('current_datetime.html',{'current_date':now})
def hours_ahead(request,offset):
	offset = offset
	time_ahead = datetime.datetime.now() + datetime.timedelta(hours=offset)
	html = "<html><body>In %s hours later, time will be <strong>%s</strong>.</body></html>" %(offset,time_ahead)
	return HttpResponse(html)



#books = {'Java':'Alex','Python':'Rachel','Ruby':'Rain'}
def book(request):
	books = {'Java':'Alex','Python':'Rachel','Ruby':'Rain'}
	return render_to_response('current_datetime.html',{'book_list':books.items()})
	
