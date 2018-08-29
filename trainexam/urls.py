"""trainexam  URL Configuration
考试学习管理工具URL转发配置
"""

from django.urls import path,include
from trainexam.views import *

urlpatterns = [
    path('',index), #首页
    path('autogenuser/',autogenuser00001),
    path('userlogin/',userlogin00001),
]
