# -*- coding: UTF-8 -*-
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class IpMachine(models.Model):
	ip = models.IPAddressField(primary_key=True)
	host_name = models.CharField(max_length=50,unique=True)
	protocol_type = models.ForeignKey('AuthMethod')
	port = models.IntegerField(max_length=7,default=22)
	opreating_system = models.CharField(max_length=30)
	group = models.ManyToManyField('IpGroup')	
	idc = models.ForeignKey('IDC', null=True, blank=True)
	#for monitor	
	def __unicode__(self):
		return self.ip
class ServerStatus(models.Model):
	host = models.IPAddressField(primary_key=True)
        host_status = models.CharField(max_length=10,default='Unkown')
        ping_status = models.CharField(max_length=100,default='Unkown')
        last_check = models.DateTimeField(auto_now_add=True)
        host_uptime = models.CharField(max_length=50,default='Unkown')
        attempt_count = models.CharField(max_length=25,null=True,blank=True)
	def __unicode__(self):
                return self.host
class IDC(models.Model):
    str_idc = models.CharField(max_length=50,unique=True)
    def __unicode__(self):
        return self.str_idc

class AuthMethod(models.Model):
	protocol = models.CharField(max_length=20)
	addtional_info = models.CharField(blank=True,max_length=50)
	def __unicode__(self):
		return self.protocol
class IpGroup(models.Model):
	group_name = models.CharField(max_length=30)
	def __unicode__(self):
		return self.group_name

class LogingUser(User):
    remote_user = models.ManyToManyField('RemoteUser', null=True, blank=True)
    group_machine = models.ManyToManyField('IpGroup', verbose_name='has access to groups',null=True, blank=True)
    ip_machine = models.ManyToManyField(IpMachine,verbose_name='has access to IP list', null=True, blank=True)

class RemoteUser(models.Model):	
	user_name = models.CharField(max_length=30)
	description = models.CharField(max_length=40,unique=True,default='mandatory,triaquae use this field to recongnize remote user')
      	password = models.CharField(default="input your remoter user password here",max_length=100)
	RsaKey_file_path = models.CharField(default="input RSA key file path if you use key to login remote server",max_length=100)
        def __unicode__(self):
                return self.description

class HostLog(models.Model):
	date = models.DateTimeField(auto_now_add=True)
	user = models.CharField(max_length=30)
	ip = models.IPAddressField()
	event_type = models.CharField(max_length=50)
	cmd = models.TextField()
	event_log = models.TextField()
	result = models.CharField(max_length=30,default='unknown')
	track_mark = models.IntegerField(blank=True)
	note = models.CharField(max_length=100,blank=True)
        def __unicode__(self):

                return self.ip

class OpsLog(models.Model):
	start_date = models.DateTimeField(auto_now_add=True)
	finish_date = models.DateTimeField(null=True,blank=True)
	log_type = models.CharField(max_length=50)
	tri_user = models.CharField(max_length=30)
	run_user = models.CharField(max_length=30)
	cmd = models.TextField()
	total_task = models.IntegerField()
	success_num = models.IntegerField()
	failed_num = models.IntegerField()
	track_mark = models.IntegerField(unique=True)	
	note = models.CharField(max_length=100,blank=True,null=True)
        def __unicode__(self):
                return self.cmd

class OpsLogTemp(models.Model):
        date = models.DateTimeField(auto_now_add=True)
        user = models.CharField(max_length=30)
        ip = models.IPAddressField()
        event_type = models.CharField(max_length=50)
        cmd = models.TextField()
        event_log = models.TextField()
        result = models.CharField(max_length=30,default='unknown')
        track_mark = models.IntegerField(blank=True)
        note = models.CharField(max_length=100,blank=True)
        def __unicode__(self):

                return self.ip
class MultiRunCounter(models.Model):
	# every time run the batch process , this field will automatically add 1,this feature is to track the multi process on WEB side
	counter = models.IntegerField(default=0)
