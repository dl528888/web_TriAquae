from django.conf.urls import patterns, url
from TriAquae.host import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<host_id>\d+)/$', views.detail, name='detail'),
    #$url(r'^diff$', views.diff, name='diff'),
    url(r'^hardware$', views.HardwareInfo),
)
