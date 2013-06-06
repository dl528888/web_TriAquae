from django.conf.urls import patterns, include, url
from TriAquae.views import TriAquae
from TriAquae.views import CpuUsage
from TriAquae.views import ServiceStatus
#from TriAquae.datas import TriAquaeData

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TriAquae.views.home', name='home'),
    # url(r'^TriAquae/', include('TriAquae.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    ('^$',TriAquae),
    ('^cpuusage/', CpuUsage),
    ('^status/', ServiceStatus),
)
