#!/usr/bin/env python

import os,time
cur_dir = os.path.dirname(os.path.abspath(__file__))
script ="time python %s/muti_ping3.py" % cur_dir

while True:
	os.system(script)
	print "+++++++sleep 15 seconds+++++++++"
	time.sleep(15)
