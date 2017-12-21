from django.shortcuts import render_to_response
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Create your views here.

class UserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=32)
    password = forms.CharField(label='密__码',widget=forms.PasswordInput())

def login(req):
    if req.method == 'POST':
        uf = UserForm(req.POST)
        if uf.is_valid():
            username1 = uf.cleaned_data['username']
            password1 = uf.cleaned_data['password']
            
            usr = authenticate(username=username1, password=password1)
            if usr is not None:
                if usr.is_active:
                    usr.login()                    
                else:
                    pass
            else:
                pass
            return HttpResponse('login.html')
            
    else:
        uf = UserForm()
        
    return render_to_response('login.html',{'uf':uf},context_instance=RequestContext(req))



def index(req):
    username = req.COOKIES.get('cookie_username','')
    return render_to_response('index.html',{'username':username})
