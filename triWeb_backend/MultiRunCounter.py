#!/usr/bin/env python

import db_connector

from web01.models import MultiRunCounter


def AddNumber():
	current_num =  MultiRunCounter.objects.all()[0]
	new_num =  current_num.counter + 1
	current_num.counter = new_num
	current_num.save()	
	return current_num.counter	
if __name__ == '__main__':
	print 'This module can not be run by it self,must be called by other programs.'
#else:
#AddNumber()
