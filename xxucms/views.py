from django.http import HttpResponse
from django.shortcuts import render_to_response

from django.contrib import auth

def index(request):
    return render_to_response('index.html',{'isok':False})



def xlogin(request):
    '''登录视图'''
    uid = request.POST.get('uid','')
    pwd = request.POST.get('pwd','')

    user = auth.authenticate(username = uid,password = pwd)
    if user is not None and user.is_active():
        auth.login(request,user)
        return render_to_response('index.html',{'uid': uid,'isok':True})    
    else:
        return render_to_response('index.html',{'uid': uid,'isok':False})
