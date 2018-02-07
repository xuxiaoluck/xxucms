"""ebook  URL Configuration
博客URL转发配置
"""

from django.urls import path,include
from eblog.views import *

urlpatterns = [
    path('',index), #首页
    path('addblog/',addblog),
    path('addblogandtype/',addblogandtype),
    path('addblogtype/',addblogtype),
]
