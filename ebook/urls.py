"""ebook  URL Configuration
电子书管理URL转发配置
"""

from django.urls import path,include
import ebook.views

urlpatterns = [
    path('',ebook.views.index), #首页 
]
