"""hiddendanger URL Configuration"""

from django.urls import path
import hiddendanger.views

"""
hiddendanger.views URL转发，在项目urls.py中include此文件，把所有
/hiddendange/** 的访问转发到本应用的视图中
"""

urlpatterns = [
    path('',hiddendanger.views.index),  #/hiddendanger/
    
]
