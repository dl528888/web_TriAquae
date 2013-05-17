#!/usr/bin/env python
#-*- coding:UTF-8 -*-
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as Login
from django.contrib.auth import logout as Logout

def login(request):
    t = get_template('login.html')

    if request.method == 'POST':
        try:
            password = request.REQUEST.get('password').encode('utf-8')
            username = request.REQUEST.get('username').encode('utf-8')
            if password and username:
                user = authenticate(username=username, password=password)
                if user is not None:
                    Login(request, user)
                    return HttpResponseRedirect("/index")
                else:
                    return HttpResponse(t.render(Context({'error':'用户名或密码错误',})))
            else:
                return HttpResponse(t.render(Context({'error':'用户名或密码不能为空',})))
        except :
            return HttpResponse(t.render(Context({'error':'用户名或密码输入错误',})))
    else:
        return HttpResponse(t.render(Context({})))

def logout(request):
    Logout(request)
    return HttpResponseRedirect('/')

def accounts(request):
    return HttpResponseRedirect('/')
