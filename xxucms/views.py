from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib import auth
from django.template.context_processors import csrf
from django.template import RequestContext
from django.contrib.auth.models import User

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


def userreg(request):
    '''点击了用户注册后的视图'''
    return render_to_response('userreg.html',{'regsave':False,'regok':False})

def regsave(request):
    '''保存注册信息视图,regsave 判断是否启动一次注册过程，regok判断是否注册成功'''

    uid = request.POST.get('username','')
    pwd = request.POST.get('password','')
    if uid == '':
        return render_to_response('userreg.html',{'idnone':'uid is null',"regsave":True})
    
    User.objects.create_user(username = uid,password = pwd,email='template@xxu.com')
    
    regsave = True
    regok = True
    return render_to_response('userreg.html',locals())
    


