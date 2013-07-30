#!/usr/bin/env python
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from web01.models import IpMachine,IpGroup,AuthMethod,RemoteUser,MultiRunCounter,LogingUser,IDC,OpsLogTemp,OpsLog,ServerStatus

import logging.config, logging, logging.handlers
logger = logging.getLogger(__name__)
class LogingUserAdmin(admin.ModelAdmin):
    fields = ('username', 'password','email', 'group_machine', 'remote_user','ip_machine')   
    list_display = ['username', 'email']
    filter_horizontal = ('group_machine','remote_user', 'ip_machine')
    list_display_links=['username','email']
    search_fields = ['username', 'email']
    #radio_fields = {'idc':admin.VERTICAL}
class IpAdmin(admin.ModelAdmin):
	list_display = ('ip','host_name','protocol_type','opreating_system','port','snmp_on')
	search_fields = ('ip','host_name','opreating_system')

class LogAdmin(admin.ModelAdmin):
	list_display = ('user','ip','event_type','cmd','event_log','result','track_mark')

class OpsLogAdmin(admin.ModelAdmin):
	list_display = ('log_type','finish_date','log_type','tri_user','run_user','cmd','total_task','success_num','failed_num','track_mark','note')
class RemoteUserAdmin(admin.ModelAdmin):
	list_display = ('user_name','description')
'''
class CdnMachineIpMachineInline(admin.TabularInline):
    model = IpMachine
    fields = ('host_name', 'ip', 'idc')
    #fk_name = IpMachine.groupmachine

class CdnMachineAdmin(admin.ModelAdmin):
    inlines = [CdnMachineIpMachineInline,]
'''

class StatusAdmin(admin.ModelAdmin):
	search_fields = ('host','host_status')
	list_display = ('host','host_status','ping_status','availability','host_uptime','breakdown_count','up_count','attempt_count')

admin.site.register(ServerStatus,StatusAdmin)
admin.site.register(OpsLogTemp,LogAdmin)
admin.site.register(OpsLog,OpsLogAdmin)
#admin.site.register(HostLog,LogAdmin)
admin.site.register(MultiRunCounter)
admin.site.register(IpMachine,IpAdmin)
admin.site.register(IpGroup)
admin.site.register(LogingUser,LogingUserAdmin)
admin.site.register(AuthMethod)
admin.site.register(RemoteUser,RemoteUserAdmin)
admin.site.register(IDC)
