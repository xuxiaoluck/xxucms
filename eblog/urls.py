"""ebook  URL Configuration
博客URL转发配置
"""

from django.urls import path,include
from eblog.views import *

urlpatterns = [
    path('',index), #首页
    path('addblogandtype/',openaddblogandtype),  #打开增加类别、博文的页面
    path('saveblog/',saveblog),
    path('addblogtype/',addblogtype),
]
