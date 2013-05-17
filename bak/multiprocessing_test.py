import time

from multiprocessing import Process


import os
'''
def info(title):
	print title
	print 'module name:', __name__
	if hasattr(os,'getppid'):
		print 'parent process:' , os.getppid()
	print 'process id:', os.getpid()

def f(name):
	info('function f')
	print 'hello', name
	time.sleep(5)

if __name__ == '__main__':
	info('main line')
	p = Process(target = f, args=('Alex',))
	p.start()
	print p.is_alive()
	print p.exitcode
	print '--------Terminate process---------'
	p.terminate()
	p.join()
	print p.exitcode
        print p.is_alive()
'''

cmd = "python  ~/sourcecode/paramiko-1.10.0/demos/demo3.py  'df'"


def batchRun(command):
	for i in range(1,50):
		os.system(command)


p = Process(target = batchRun, args = (cmd,))
p.start()

