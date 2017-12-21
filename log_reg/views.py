from django.shortcuts import render
from django import forms
from django import user

# Create your views here.

class UserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=100)
    password = forms.CharField(label='密__码',widget=forms.PasswordInput())

def login(req):
    if req.method == 'POST':
        uf = UserForm(req.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            #对比输入的用户名和密码和数据库中是否一致
            userPassJudge = user.objects.filter(username__exact=username,password__exact=password)

            if userPassJudge:
                response = HttpResponseRedirect('/index/')
                response.set_cookie('cookie_username',username,3600)
                return response
            else:
                return HttpResponse('login.html')
    else:
        uf = UserForm()
    return render_to_response('login.html',{'uf':uf},context_instance=RequestContext(req))



def index(req):
    username = req.COOKIES.get('cookie_username','')
    return render_to_response('index.html',{'username':username})
