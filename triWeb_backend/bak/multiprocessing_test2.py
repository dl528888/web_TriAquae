

import multiprocessing 

import time

def func(msg):
	'''for i in xrange(5):
		print msg
		time.sleep(1)
	'''
	print msg
	time.sleep(1)	

pool = multiprocessing.Pool(processes=12)
result = []
for i in xrange(10):
	msg = "hello %d" % i
	result.append(pool.apply_async(func,(msg,)))
	#print '----- %d -----' % i
pool.close()
pool.join()

for res in result:
	print res.get()
print "Sub-process done."
