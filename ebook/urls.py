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
    #path('addauthor/',ebook.views.addauthor),
    path('addbooks/',ebook.views.addbooks),
    path('uploadfiles/',ebook.views.uploadfiles),
    path('booklistbytypename/',ebook.views.booklistbytypename),   #按类别名称列出一类书籍数据
    path('downloadfile/',ebook.views.downloadfile),  #下载文件到本地
    path('modifybook/',ebook.views.modifybook),
]
