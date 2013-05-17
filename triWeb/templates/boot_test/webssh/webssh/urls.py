#!/usr/bin/env python
#-*- coding:UTF-8 -*-
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
     (r'^$', 'lib.login.login'),
     (r'^index$', 'lib.main.index'),
     (r'^login$', 'lib.login.login'),
     (r'^logout$', 'lib.login.logout'),
     (r'^add$', 'lib.main.add'),
     (r'^change$', 'lib.main.change'),
     (r'^show$', 'lib.main.show'),
     (r'^update$', 'lib.main.update'),
     (r'^delete$', 'lib.main.delete'),
     (r'^pssh$', 'lib.main.pssh'),
     (r'^about$', 'lib.main.about'),
     (r'^accounts/', 'lib.login.accounts'),
     (r'^static/(?P<path>.*)$', 'django.views.static.serve'),
)
