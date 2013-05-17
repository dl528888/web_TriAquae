#!/usr/bin/env python
#-*- coding:UTF-8 -*-
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from lib.models import Servers
from lib.pssh import runcmd

@login_required()
def index(request):
    t = get_template("index.html")
    return HttpResponse(t.render(Context({})))

@login_required()
def add(request):
    t = get_template("add.html")
    if request.method == 'POST':
        try:
            data = Servers(
                ip=request.REQUEST.get("ip"),
                username=request.REQUEST.get("username"),
                password=request.REQUEST.get("password"),
                hostname=request.REQUEST.get("hostname"),
                port=request.REQUEST.get("port"),
                )
            data.save()
            return HttpResponse(t.render(Context({'info':"添加成功"})))
        except :
            return HttpResponse(t.render(Context({'info':"添加失败"})))
    
    return HttpResponse(t.render(Context({})))

@login_required()
def change(request):
    t = get_template("change.html")
    data = Servers.objects.all()
    return HttpResponse(t.render(Context({'data':data})))

@login_required()
def about(request):
    t = get_template('about.html')
    return HttpResponse(t.render(Context({})))

@login_required()
def show(request):
    t = get_template("show.html")

    if request.method == "POST":
        id = request.REQUEST.get('id')
        print id
        d = Servers.objects.filter(id=id)
        
        if d:
            return HttpResponse(t.render(Context({'data':d[0]})))
        else:
            return HttpResponse(t.render(Context({'info':"错误！"})))

@login_required()
def update(request):
    t = get_template("change.html")

    if request.method == "POST":
        id = request.REQUEST.get("id")
        try:
            s = Servers.objects.get(id=id)
            s.hostname = request.REQUEST.get('hostname')
            s.ip = request.REQUEST.get('ip')
            s.username = request.REQUEST.get('username')
            s.password = request.REQUEST.get('password')
            s.port = request.REQUEST.get('port')
            s.save()
            data = Servers.objects.all()
            return HttpResponse(t.render(Context({'data':data, 'info':"修改成功", 'id':int(id)})))
        except :
            data = Servers.objects.all()
            return HttpResponse(t.render(Context({'data':data ,'info':"修改失败", 'id':id})))

@login_required()
def delete(request):
    t = get_template("change.html")

    if request.method == "POST":
        id = request.REQUEST.get("id")
        try:
            Servers.objects.filter(id=id).delete()
            data = Servers.objects.all()
            return HttpResponse(t.render(Context({'data':data})))
        except :
            data = Servers.objects.all()
            return HttpResponse(t.render(Context({'data':data, 'info':"删除失败", 'id':id})))

@login_required()
def pssh(request):
    id = []
    for i in request.GET:
        try:
            id.append(int(i))
        except:
            pass

    cmd = request.GET.get("cmd")
    if cmd and id:
        servers = []
        for i in id:
            servers.append(Servers.objects.filter(id=i)[0])
        result = runcmd(servers, cmd)

        t = get_template("result.html")
        return HttpResponse(t.render(Context({'result':result})))
    
    t = get_template("pssh.html")
    data = Servers.objects.all()
    return HttpResponse(t.render(Context({'data':data})))
