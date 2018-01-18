"""ebook  URL Configuration
电子书管理URL转发配置
"""

from django.urls import path,include
import ebook.views

urlpatterns = [
    path('',ebook.views.index), #首页
    path('uploadbook/',ebook.views.addbooks),
    path('addpublisher/',ebook.views.addpublisher),  #增加一个出版社
    path('addbooktype/',ebook.views.addbooktype),
    path('addauthor/',ebook.views.addauthor),
]
