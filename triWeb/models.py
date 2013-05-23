from django.db import models
from django import forms
from datetime import datetime
# Create your models here.


class Group(models.Model):
        group_name = models.CharField(max_length=30)
	parent_group = models.CharField(max_length=30,default="TOPGROUP")
	#sub_group_of = models.ForeignKey(Group)	
	def __unicode__(self):
                #return u'%s %s' %(self.group_name,self.parent_group)
		return self.group_name

class User(models.Model):
        user_name = models.CharField(max_length=30)
        email   = models.EmailField()
        phone   = models.IntegerField(max_length=13)
        group_name = models.ManyToManyField(Group,verbose_name='Member of groups')
	access_ip_list = models.ManyToManyField('IP',verbose_name = "Access IP list")
        RSA_KEY_file = models.CharField(max_length=100)
        def __unicode__(self):
                return self.user_name
class MonitorMethod(models.Model):
        monitor_method = models.CharField(max_length = 20,default="ping")
        version = models.CharField(max_length = 20)
	def __unicode__(self):
		return self.monitor_method

class ConnectionMethod(models.Model):
        protocol = models.CharField(max_length=20)
        addtional_info = models.CharField(blank=True,max_length=100)
	
	def __unicode__(self):
		return self.protocol

class IP(models.Model):
	ip = models.IPAddressField(primary_key=True)
	username = models.CharField(max_length=20)
	password2 = forms.CharField(max_length=32,widget=forms.PasswordInput)
	password = models.CharField(max_length=128)
	server_name = models.CharField(max_length=50,unique=True)

	protocol_type = models.ForeignKey(ConnectionMethod,null=True)
	port = models.IntegerField(max_length=7,default=22)
	
	opreating_system = models.CharField(max_length=30)
	status	= models.CharField(max_length = 10)
	agent = models.CharField(max_length = 20,default="NO")
	group_name = models.ManyToManyField(Group,related_name = 'GroupZone')
	online_date = models.DateField(blank=True)
	#updated_at  = models.DateTimeField(blank=True)
	description = models.CharField(blank=True,max_length=50)
	creater	=	models.ForeignKey(User)
	monitor_status = models.ForeignKey(MonitorMethod)
	ping_status = models.CharField(max_length=100,null=True)
        def __unicode__(self):
                return self.ip

'''
class User(models.Model):
        user_name = models.CharField(max_length=30)
        email   = models.EmailField()
        phone   = models.IntegerField(max_length=13)
        group_name = models.ManyToManyField(Group,verbose_name='Member of groups')
        access_ip_list = models.ManyToManyField(IP,verbose_name = "Access IP list")
	RSA_KEY_file = models.CharField(max_length=100)

        def __unicode__(self):
                return self.user_name
'''
class MonthlyWeatherByCity(models.Model):
	month = models.IntegerField()
	Bejing_temp= models.DecimalField(max_digits=5,decimal_places=1)
	ShangHai_temp = models.DecimalField(max_digits=5,decimal_places=1)
class DailyWeather(models.Model):
	month = models.IntegerField()
	day = models.IntegerField()
	temperature = models.DecimalField(max_digits=5,decimal_places=2)
	rainfall = models.DecimalField(max_digits=5,decimal_places=1)
	city = models.CharField(max_length=50)
	state = models.CharField(max_length=2)
class PingStatusValue(models.Model):
	ip = models.ForeignKey(IP)
	check_time =  models.DateTimeField()
	ping_value = models.DecimalField(max_digits=5,decimal_places=2,null=True)
	def __unicode__(self):
		return str(self.ip)

class HostLog(models.Model):
	date = models.DateTimeField(auto_now_add=True)
	user = models.CharField(max_length=30)
	ip = models.IPAddressField()
	event_type = models.CharField(max_length=50)
	cmd = models.TextField()
	event_log = models.TextField()
	result = models.CharField(max_length=30,default='unkown')
	track_mark = models.IntegerField(blank=True)
	note = models.CharField(max_length=100,blank=True)
class MultiRunCounter(models.Model):
	# every time run the batch process , this field will automatically add 1,this feature is to track the multi process on WEB side
	counter = models.IntegerField(default=0)
