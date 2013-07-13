#!/usr/bin/env python

import sys,os,time
sys.path.append('/home/alex/py_training/py_web')
os.environ['DJANGO_SETTINGS_MODULE'] ='py_web.settings'
#----------------Use Django Mysql model----------------
from py_web import settings
from  web01.models import * 
