import sys,os
from datetime import *
sys.path.append('/home/alex/Django-1.5/django/bin/mysite')
os.environ['DJANGO_SETTINGS_MODULE'] ='mysite.settings'

from django.core.management import setup_environ
from mysite import settings

from  triWeb.models  import IP,Group

#setup_environ(settings)

#-------------------------------

ip_list = IP.objects.all()

for ip in ip_list:
	print ip,ip.status
