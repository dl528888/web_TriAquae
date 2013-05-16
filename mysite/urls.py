from django.conf.urls import patterns, include, url
from mysite.view import current_datetime,hours_ahead
from triWeb import views,contact,runCmd,group,hostDetail,graph
from triWeb import boot_login

from triWeb import batchAddServer,monitor
#from django.views.generic.simple import redirect_to
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
	(r'^site_media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT,}),
    #(r'^time/$', current_datetime),
    #(r'^time/plus/(\d{1,24})/$', hours_ahead),
    #(r'^ua/',ua1),
    #(r'^ua2/',display_meta),
	#(r'^search-form/$',views.search_form),
	#(r'^search/$',views.search2),
	#(r'^showFile/$',views.displayFile),
	#(r'^contact/$',contact.Contact),	
	(r'^runCmd/$',runCmd.runCMD),
	#(r'^getCmd/$',runCmd.getCMD),
	(r'^server_list/$', runCmd.ShowServerList),
	(r'^dashboard/$', runCmd.dashboard),

	(r'^monitorPage/$', views.ShowIP),
	(r'^monitor/$', monitor.server_status),
	(r'^addServers/$', batchAddServer.addServer),
	
	#for Ajax
	(r'^ajax/test/$', views.ajaxTest),
	(r'^loadcd/$', views.loadCD),

	(r'^groupSummary/$',group.groupSummary),
	(r'^hostDetail/$', hostDetail.host_detail),
	(r'^navigation_overview/$', hostDetail.navigation),
	(r'^graph/$', hostDetail.graphs),
	(r'^highchart/$',graph.weather_chart_view),
	(r'^highchart2/$',graph.ping_status_view),
	#----------for bootstrap-------
	(r'^login/$', boot_login.login),
	(r'^static/(?P<path>.*)$', 'django.views.static.serve'),
)
