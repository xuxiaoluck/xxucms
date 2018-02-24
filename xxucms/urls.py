"""xxucms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
import xxucms.views
import ebook.urls
import eblog.urls

urlpatterns = [
    path('',xxucms.views.index),
    path('test/',xxucms.views.test),  #测试单元
    path('home/',xxucms.views.index), #所有的地方点击了回首页按钮
    path('admin/', admin.site.urls),
    path('login/',xxucms.views.xlogin),
    path('logout/',xxucms.views.xlogout),
    path('userreg/',xxucms.views.userreg),   #index中点了用户注册
    path('regsave/',xxucms.views.regsave),   #userreg.html中点击了注册按钮
    path('ebook/',include(ebook.urls)),
    path('eblog/',include(eblog.urls)),
]
