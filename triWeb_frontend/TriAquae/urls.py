#from django.conf.urls import patterns, include, url
from django.conf.urls import *
from TriAquae.views import TriAquae
from TriAquae.views import CpuUsage
from TriAquae.views import ServiceStatus
#from TriAquae.datas import TriAquaeData
from TriAquae.views import TriAquae, Command_Execution, File_Transfer, Server_Configuration, Job_Schedule, Assets_Management
from views import GetServers
from host.views import runCmd, cmd_result,AllUsers,AllCommands,stopExecution,getFailedLists,loadFileTransferPage


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TriAquae.views.home', name='home'),
    # url(r'^TriAquae/', include('TriAquae.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',TriAquae),
    url(r'^cpuusage/', CpuUsage),
    url(r'^status/', ServiceStatus),
    url(r'^command_execution$',Command_Execution),
    url(r'^file_transfer$',File_Transfer),
    url(r'^server_configuration$',Server_Configuration),
    url(r'^job_schedule$',Job_Schedule),
    #url('^assets_management$',Assets_Management),
    url(r'^host/',include('TriAquae.host.urls',namespace='host')),
    url(r'^GetServers$',GetServers),
    url(r'^runCmd/$',runCmd),
    url(r'^cmd_result/$',cmd_result),
    url(r'^AllCommands/$',AllCommands),
    url(r'^AllUsers/$',AllUsers),
    url(r'^stopExecution/$',stopExecution),
    url(r'^getFailedLists/$',getFailedLists),
    url(r'^loadFileTransferPage/$',loadFileTransferPage),
)
