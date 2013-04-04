import multiprocessing
import sys,os,time
sys.path.append('/home/alex/Django-1.5/django/bin/mysite')
os.environ['DJANGO_SETTINGS_MODULE'] ='mysite.settings'
#----------------Use Django Mysql model----------------
from mysite import settings
from  triWeb.models import IP,Group,HostLog
import MultiRunCounter

run_user = "MultiRunCmdTestUser"
track_num = MultiRunCounter.AddNumber()
script = 'python  ~/triWeb_dev/run_command2.py'
ip_list = IP.objects.all()

host_list = sys.argv[1]
cmd= sys.argv[2]
#run_user = sys.argv[3]

# batch run process
result = []
def run(host):
	task = '''%s %s '%s' %s %s''' % (script,host,cmd,track_num,run_user)
	os.system(task)

pool = multiprocessing.Pool(processes=20)

for ip in ip_list:
	result.append(pool.apply_async(run,(ip,)) )
#time.sleep(5)
#pool.terminate()

pool.close()
pool.join()


for res in result:
	res.get(timeout=5)
