from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib import auth
from django.template.context_processors import csrf
from django.template import RequestContext


def index(request):
    return render_to_response('index.html',{'isok':False})

def xlogin(request):
    '''登录视图'''
    uid = request.POST.get('uid','')
    pwd = request.POST.get('pwd','')
    user = auth.authenticate(username = uid,password = pwd)
    isok = True
    if user is not None and user.is_active:
        auth.login(request,user)
        return render_to_response('index.html',locals())
    else:
        isok = False
        return render_to_response('index.html',locals())

def xlogout(request):
    auth.logout(request)
    return render_to_response('index.html',locals())


