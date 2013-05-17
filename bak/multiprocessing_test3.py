import multiprocessing
import sys,os,time
sys.path.append('/home/alex/Django-1.5/django/bin/mysite')
os.environ['DJANGO_SETTINGS_MODULE'] ='mysite.settings'
#----------------Use Django Mysql model----------------
from mysite import settings
from  triWeb.models import IP,Group

script = 'python  ~/triWeb_dev/demo3.py'
ip_list = IP.objects.all()


command= sys.argv[1]

result = []
def run(host):
	cmd = '''%s %s '%s' ''' % (script,host,command)
	os.system(cmd)
#run(sys.argv[1])	

pool = multiprocessing.Pool(processes=20)
for ip in ip_list:
	result.append(pool.apply_async(run,(ip,)) )
#time.sleep(5)
#pool.terminate()

pool.close()
pool.join()

for res in result:
	print res.get(timeout=5)

