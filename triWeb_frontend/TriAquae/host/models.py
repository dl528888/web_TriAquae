from django.db import models
from django import forms

# start by zp
# Create your models here.
class Host(models.Model):
    host = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=64, unique=True)
    alias = models.CharField(max_length=64, null=True)
    group = models.CharField(max_length=64, null=True)
    platform = models.CharField(max_length=64)
    platform_full = models.CharField(max_length=255, null=True)
    model = models.CharField(max_length=64, null=True)
    hw_cpu = models.CharField(max_length=255, null=True)
    hw_memory = models.CharField(max_length=64, null=True)
    macaddress_a = models.CharField(max_length=64, null=True)
    macaddress_b = models.CharField(max_length=64, null=True)
    hw_full = models.TextField(null=True)
    location = models.CharField(max_length=255, null=True)
    vendor = models.CharField(max_length=64, null=True)
    supplier = models.CharField(max_length=64, null=True)
    contact_number = models.CharField(max_length=64, null=True)
    purchase_date = models.DateField('purchase date', null=True)
    expiry_date = models.DateField('expiry date', null=True)
    serialno_a = models.CharField(max_length=64, null=True)
    serialno_b = models.CharField(max_length=64, null=True)
    tag = models.CharField(max_length=64, null=True)
    notes = models.TextField(null=True)

    def __unicode__(self):
        return self.name

    #class Meta:
    #    db_table='customer'

class HostForm(forms.ModelForm):
    host = forms.CharField(max_length=64)
    name = forms.CharField(max_length=64)
    alias = forms.CharField(max_length=64)
    group = forms.CharField(max_length=64)
    platform = forms.CharField(max_length=64)
    platform_full = forms.CharField(max_length=255)
    model = forms.CharField(max_length=64)
    hw_cpu = forms.CharField(max_length=255)
    hw_memory = forms.CharField(max_length=64)
    macaddress_a = forms.CharField(max_length=64)
    macaddress_b = forms.CharField(max_length=64)
    hw_full = forms.CharField(max_length=64)
    location = forms.CharField(max_length=255)
    vendor = forms.CharField(max_length=64)
    supplier = forms.CharField(max_length=64)
    contact_number = forms.CharField(max_length=64)
    purchase_date = forms.DateField()
    expiry_date = forms.DateField()
    serialno_a = forms.CharField(max_length=64)
    serialno_b = forms.CharField(max_length=64)
    tag = forms.CharField(max_length=64)
    notes = forms.CharField()
#end by zp

#start by tangjing
class IP(models.Model):
    ip = models.IPAddressField(primary_key=True)
    server_name = models.CharField(max_length=50,unique=True)
    protocol_type = models.ForeignKey('auth_method')
    port = models.IntegerField(max_length=7,default=22)
    opreating_system = models.CharField(max_length=30)
    group = models.ManyToManyField('Group')
    status = models.CharField(max_length=10)
    def __unicode__(self):
            return self.ip

class auth_method(models.Model):
    protocol = models.CharField(max_length=20)
    addtional_info = models.CharField(blank=True,max_length=50)
    def __unicode__(self):
                return self.protocol
class Group(models.Model):
    group_name = models.CharField(max_length=30)
    def __unicode__(self):
            return self.group_name


class remote_user(models.Model):
    user_name = models.CharField(max_length=30)
    description = models.CharField(max_length=40)
    password = models.CharField(default="input your remoter user password here",max_length=100)
    RsaKey_file_path = models.CharField(default="input RSA key file path if you use key to login remote server",max_length=100)
    def __unicode__(self):
            return self.user_name

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

class MultiRunCounter(models.Model):
    # every time run the batch process , this field will automatically add 1,this feature is to track the multi process on WEB side
    counter = models.IntegerField(default=0)

#end by tangjing


