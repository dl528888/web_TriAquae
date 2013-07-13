from django.template.loader import get_template
from django.template import Template, Context
from django.http import HttpResponse
from TriAquae.host.models import Host

import random
from collections import OrderedDict

from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from host.models import Group,IP,remote_user,HostLog
import datetime
from django.contrib import auth
import os,time
from TriAquae.host.backend import MultiRunCounter





try:
    import json
except:
    import simplejson as json


def TriAquae(request):
    t = get_template('index.html')
    # theme = "- Easy to Admin (v2.0.0)"

    html = t.render(Context({'theme': '- Easy to Admin (v2.0.0)'}))
    return HttpResponse(html)

def Command_Execution(request):
    t = get_template('command_execution.html')
    #html=t.render(Context({'form_name':'Enter your command:'}))
    html=t.render(Context())
    return HttpResponse(html)


def File_Transfer(request):
    t = get_template('file_transfer.html')
    html=t.render(Context())
    return HttpResponse(html)


def Server_Configuration(request):
    t = get_template('server_configuration.html')
    html=t.render(Context())
    return HttpResponse(html)


def Job_Schedule(request):
    t = get_template('job_schedule.html')
    html=t.render(Context())
    return HttpResponse(html)


def Assets_Management(request):
    t = get_template('assets_management.html')
    html=t.render(Context())
    return HttpResponse(html)


def CpuUsage(request):
    dict_r = OrderedDict()
    random.seed()
    for i in range(24):
        now_i = '%d:05' % i
        val_i = random.randint(0, 100)
        dict_r[now_i] = val_i
    return HttpResponse(json.dumps(dict_r))


def ServiceStatus(request):
    from datas import getStatus
    dict_s = getStatus()
    dict_status = dict_s['services']
    if request.is_ajax():
        return HttpResponse(json.dumps(dict_status), mimetype="application/json")
    else:
        t = get_template('status.html')
        ss_summary = {
            'status': {
                'Ok': 0,
                'Critical': 0,
                'Warning': 0,
                'Unknown': 0,
                'Pending': 0
            },
            'handled': {
                'Unhandled': 0,
                'Problems': 0,
                'All': 0
            }
        }
        ss_detail = []
        for service in dict_status:
            ss_summary['handled']['All'] += 1
            status = service['Status']
            ss_summary['status'][status] += 1
            cell = []
            for k, v in service.iteritems():
                cell.append(v)
            ss_detail.append({'cell': cell})

        var_service_status = get_template('servicestatus.html').render(Context({
            'ss_summary_handled': ss_summary['handled'],
            'ss_summary_status': ss_summary['status'],
            'ss_detail': json.dumps(ss_detail)
        }))
        html = t.render(Context({
            'var_service_status': var_service_status
        }))
        return HttpResponse(html)


def ServiceStatus(request):
    from datas import getStatus
    dict_s = getStatus()
    dict_status = dict_s['services']
    if request.is_ajax():
        return HttpResponse(json.dumps(dict_status), mimetype="application/json")
    else:
        t = get_template('status.html')
        ss_summary = {
            'status': {
                'Ok': 0,
                'Critical': 0,
                'Warning': 0,
                'Unknown': 0,
                'Pending': 0
            },
            'handled': {
                'Unhandled': 0,
                'Problems': 0,
                'All': 0
            }
        }
        ss_detail = []
        for service in dict_status:
            ss_summary['handled']['All'] += 1
            status = service['Status']
            ss_summary['status'][status] += 1
            cell = []
            for k, v in service.iteritems():
                cell.append(v)
            ss_detail.append({'cell': cell})

        var_service_status = get_template('servicestatus.html').render(Context({
            'ss_summary_handled': ss_summary['handled'],
            'ss_summary_status': ss_summary['status'],
            'ss_detail': json.dumps(ss_detail)
        }))
        html = t.render(Context({
            'var_service_status': var_service_status
        }))
        return HttpResponse(html)

#start by tangjing
def GetServers(request):
    data = []
    counter = 0
    group_list  = Group.objects.all()
    for g_name in group_list:
            counter += 1
            data.append({'id': counter, 'pid':0, 'text':g_name.group_name, 'bgroup':1})
            ip_list =  IP.objects.filter(group__group_name = g_name.group_name)
            ip_counter = 0
            for ip in ip_list:
                    ip_counter += 1
                    data.append({'id':'%s%s'%(counter,ip_counter), 'pid': counter, 'text':ip.server_name, 'bgroup':0 , 'ip':ip.ip })

    '''data=[
    { 'id':1,'pid':0, 'text': 'Node 1','bgroup':1},
    { 'id':11,'pid':1, 'text': 'Node 1.1','bgroup':0},
    { 'id':12,'pid':1, 'text': 'Node 1.2','bgroup':0},
    { 'id':2,'pid':0,'text': 'Node 2' ,'bgroup':0},
    { 'id':3,'pid':0,'text': 'Node 3' ,'bgroup':0},
    { 'id':4,'pid':0,'text': 'Node 4' ,'bgroup':0},
    { 'id':5,'pid':0,'text': 'Node 5' ,'bgroup':0},
    ];'''
    #data=[{'a':'b'}]
    return HttpResponse(json.dumps(data));
#end by tangjing


