#!/usr/bin/env python

import db_connector

user_list = db_connector.LogingUser.objects.all()

can_access_dic = {} 
for u in user_list:
	can_access_dic[u.email] = []
	for i in u.ip_machine.all():
		can_access_dic[u.email].append( i.ip )
	for g in u.group_machine.all():
		 for i in g.ipmachine_set.all():
			can_access_dic[u.email].append(i.ip)

#print can_access_dic
