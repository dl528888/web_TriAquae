import sys,os
from datetime import *
sys.path.append('/home/alex/Django-1.4.3/django/bin/mysite')
os.environ['DJANGO_SETTINGS_MODULE'] ='mysite.settings'

from django.core.management import setup_environ
from mysite import settings

from triWeb.models import IP,MonthlyWeatherByCity,PingStatusValue
import time
setup_environ(settings)
#-------------------------------
'''
ip_list = IP.objects.all()

for ip in ip_list:
	print ip,ip.status

MonthlyWeatherByCity(models.Model):
	month = models.IntegerField()
	Bejing_temp= models.DecimalField(max_digits=5,decimal_places=1)
	ShangHai_temp = models.DecimalField(max_digits=5,decimal_places=1)
f = file('/tmp/data.txt')
while True:
	line = f.readline()
	if len(line) == 0:break
	d = line.split()
	#print d[0],d[1],d[2]
	MonthlyWeatherByCity.objects.create(month=d[0],Bejing_temp=d[1],ShangHai_temp=d[2]) 
------------
num = 1
for i in range(1,1000):
	for ip in IP.objects.all():
		print '---------------------------------------Added:',ip,'---------item:',num
		num +=1
		PingStatusValue.objects.create(ip=ip,ping_value='9.14')
	time.sleep(0.10)'''


list= IP.objects.filter(ip=IP.objects.get(ip='8.8.8.8'))

for i in list:
	print list
