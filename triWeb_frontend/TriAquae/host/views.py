from django.shortcuts import render, get_object_or_404, RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.http import Http404
from models import Host, HostForm

from django.http import HttpResponse,HttpResponseRedirect
from django.template import Template,Context
from django.shortcuts import render_to_response
from django.template import RequestContext
from .models import Group,IP,remote_user,HostLog
import datetime
from django.contrib import auth
import os,time
from .backend import MultiRunCounter


import random
from collections import OrderedDict
try:
    import json
except:
    import simplejson as json


def index(request):
    latest_host_list = Host.objects.order_by('-host')[:5]
    context = { 'latest_host_list':latest_host_list }
    #return render(request, 'index.html', context)
    return render(request, 'assets_management.html', context)


def detail(request, host_id):
    host = Host.objects.get(pk=host_id)
    if request.method == "POST":
        form = HostForm(request.POST, instance=host)
        if form.is_valid():
            #host = form.cleaned_data['host']
            #name = form.cleaned_data['name']
            #alias = form.cleaned_data['alias']
            form.save()
            #return HttpResponseRedirect('/detail/')
            return HttpResponseRedirect('assets_management.html')
            #return HttpResponseRedirect(reverse('Welcome'))
    else:
        form = HostForm(instance=host)

    #return render(request, 'assets_detail.html', {'host':host, 'form':form})
    return render(request, 'assets_detail.html', {'host':host, 'form':form}, context_instance=RequestContext(request))

#def diff(request):
#    dict_r = OrderedDict()
#    random.seed()
#    for i in range(24):
#        now_i = '%d:05' % i
#        val_i = random.randint(0, 100)
#        dict_r[now_i] = val_i
#    #return render(request, 'assets_detail.html', {'dict_r':json.dumps(dict_r['0:05'])})
#    return render(request, 'assets_diff.html')
#    #return HttpResponse(request, 'assets_diff.html', {'dict_r':json.dumps(dict_r['0:05'])})
#    #return HttpResponse(json.dumps(dict_r))
#    #return HttpResponse("you're looking at diff info of hosts")

def HardwareInfo(request):
    dict_r = OrderedDict()
    random.seed()
    for i in range(24):
        now_i = '%d:05' % i
        val_i = random.randint(0, 100)
        dict_r[now_i] = val_i
    #return HttpResponse(json.dumps(dict_r))
    #context = {'dict_r[now_0]':dict_r[val_0'}
    return render(request, 'detail.html', {'dict_r':json.dumps(dict_r['0:05'])})



#def contact(request):
#    form = ContactForm()
#    if request.method == "POST":
#        form = ContactForm(request.POST or None)
#        if form.is_valid():
#            host = form.cleaned_data['host']
#            form.save()
#            return HttpResponseRedirect('/host/contact/')
#        #else:
#            #form = ContactForm()
#
#    return render(request, 'contact.html', {'form': form})


#start by tangjing

def login(request):
    return render_to_response('login.html')

def account_login(request):
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    user = auth.authenticate(username=username,password=password)
    if user is not None: #and user.is_active:
        #correct password and user is marked "active"
        auth.login(request,user)
        return HttpResponseRedirect("/hello/")
    else:
        return render_to_response('login.html',{'login_err':'Wrong username or password!'})

def logout_view(request):
    user = request.user
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponse("%s logged out!" % user)
def hello(request):
    if request.user.is_authenticated() is None:
        return HttpResponse("User not login yet!!!")
    else:

        now = datetime.datetime.now()
        group_list ={}
        for group in Group.objects.all():
                ip_nums_in_group = IP.objects.filter(group__group_name = group)
                group_list[group] = ip_nums_in_group

        return render_to_response("boot1.html",{'group_list':group_list, 'user':request.user})
        #return render_to_response('hello.html',{'current_date': now} )

def batch_management(request):
    if request.user.is_authenticated() is None:
        return HttpResponse("User not login yet!!!")
    else:

        now = datetime.datetime.now()
        group_list ={}
        for group in Group.objects.all():
                ip_nums_in_group = IP.objects.filter(group__group_name = group)
                group_list[group] = ip_nums_in_group
        remote_users = remote_user.objects.all()
        return render_to_response("BatchManagement.html",{'group_list':group_list, 'user':request.user,'r_users':remote_users})

def cmd_result(request):
    if (1):
        #if request_method == "GET":
        track_id = request.GET['TrackMark']
        total_tasks = request.GET['TotalTasks']
        success_tasks = len(HostLog.objects.filter(track_mark = int(track_id),result='Success'))
        failed_tasks = len(HostLog.objects.filter(track_mark = int(track_id),result='Error'))
        cmd_log = file('/usr/local/src/triWeb_frontend/TriAquae/hosts/backend/track_run_num_12.log')

        t = Template(
        '''
        \n<h4>TotalTasks:<span id="total_num">{{total_tasks}}</span> <a href= "javascript:void(0)">Success:<span id="sucnum"> {{success_tasks}}</span></a> <a href="javascript:void(0)">Failed:
        \n<span id="failnum">{{failed_tasks}}</span></a></h4>
        \n<div>{{cmd_log}}</div>
        '''
        )

        cmd_ret = cmd_log.read()

        html = t.render(Context({'cmd_log':cmd_ret,'total_tasks':total_tasks, 'success_tasks': success_tasks, 'failed_tasks': failed_tasks}))
        cmd_log.close()
    return HttpResponse(html)
    #return HttpResponse('{"success_tasks":%s,"failed_tasks":%s,"cmd_log":[%s]}' %(success_tasks,failed_tasks,cmd_ret))

def get_groupList(request):
    if request.is_ajax():
        #if request_method == "GET":
        G_name = request.GET['Name']
        ip_list = IP.objects.filter(group__group_name = G_name)

    return render_to_response('server_list.html',{"ip_list_of_group":ip_list},context_instance=RequestContext(request))


def runCmd(request):
    group_list = Group.objects.all()
    checked_group_list = []
    ip_list = []
    for g_name in group_list:
            if request.POST.get(g_name.group_name):
                    checked_group_list.append(g_name)
                    for ip in  IP.objects.filter(group__group_name = g_name):
                            ip_list.append(ip.ip)
    task_num = len(ip_list)
    ip_list_to_string = ' '.join(ip_list)
    track_mark = MultiRunCounter.AddNumber()
    user_input = request.POST['command']
    user_account = request.POST['UserName']
    iplists = request.POST['IPLists']
    print "user inputs command is: %s and username is:%s and iplists are: %s" %(user_input,user_account,iplists)
    cmd = "python /usr/local/src/triWeb_frontend/TriAquae/hosts/backend/multiprocessing_runCMD.py '%s' '%s'alex %s %s &" % (ip_list_to_string,user_input,track_mark,os.listdir('.'))
    os.system(cmd)
    #return render_to_response('runCmd.html',{"checked_group":checked_group_list,"input_cmd":user_input},context_instance=RequestContext(request))
    #return render_to_response('auto_load.html',{"checked_group":checked_group_list,"input_cmd":user_input,'cmd':cmd ,'track_mark':track_mark})
    #return render_to_response('auto_load.html',{'track_mark':track_mark, 'task_num': task_num})
    return HttpResponse('{"TrackMark":%s, "TotalNum":%s}' %(track_mark, task_num))

def getFailedLists(request):
    return HttpResponse('["10.2.3.4","10.2.3.5"]')

def AllUsers(request):
    #loginuser = request.GET['LoginUser']
    user_list =remote_user.objects.all()
    u_list = []
    for user in user_list:
            u_list.append(user.user_name)
    return HttpResponse(json.dumps(u_list))

def AllCommands(request):
    #allcommands = ["df","iostat","shutdown","restart"]
    #return HttpResponse('["df","iostat","shutdown","restart"]')
    cmd_list = os.popen('bash /usr/local/src/triWeb_frontend/TriAquae/hosts/backend/command_list.sh').read()
    #commands = cmd_list.split('\n')
    print cmd_list
    return HttpResponse(cmd_list)


def stopExecution(request):
    trackmark = request.GET['TrackMark']
    #todo
    return HttpResponse("stop successfully")

def loadFileTransferPage(request):
    #todo
    return render_to_response("mulSelector.html")
#end by tangjing



