import multiprocessing
import sys,os
sys.path.append('/home/alex/Django-1.5/django/bin/mysite')
os.environ['DJANGO_SETTINGS_MODULE'] ='mysite.settings'
#----------------Use Django Mysql model----------------
#from mysite import settings
#from  triWeb.models import IP,Group

script = 'python  ~/sourcecode/paramiko-1.10.0/demos/demo_batch.py'
#ip_list = IP.objects.all()

result = []
def run(host,cmd):
	os.system("%s %s %s"% (script,host,cmd) )

#run(sys.argv[1])	

#pool = multiprocessing.Pool(processes=200)
pool = multiprocessing.Pool(processes=60)
f = file('/tmp/hosts2')
while True:
	ip2 = f.readline() 
	if len(ip2) ==0:break
	ip = ip2.split()[0]
	result.append(pool.apply_async(run,(ip,sys.argv[1],)) )
pool.close()
pool.join()

for res in result:
	print res.get()

