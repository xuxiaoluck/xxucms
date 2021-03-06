"""ebook  URL Configuration
电子书管理URL转发配置
"""

from django.urls import path,include
import ebook.views

urlpatterns = [
    path('',ebook.views.index), #首页
    path('openaddbookandtype/',ebook.views.openaddbookandtype), 
    path('addpublisher/',ebook.views.addpublisher),  #增加一个出版社
    path('addbooktype/',ebook.views.addbooktype),
    path('addbooks/',ebook.views.addbooks),
    path('uploadfiles/',ebook.views.uploadfiles),
    path('booklistbytypename/',ebook.views.booklistbytypename),   #按类别名称列出一类书籍数据
    path('downloadfile/',ebook.views.downloadfile),  #下载文件到本地
    path('modifybook/',ebook.views.modifybook),
    path('deleteonebookfile/',ebook.views.deleteonebookfile),
    path('deleteonebook/',ebook.views.deleteonebook),
    path('showbooktypelist/',ebook.views.showbooktypelist), #2018－09－07改，加载分类列表数据到表格
    path('showbooklist/',ebook.views.showbooklist),
    path('showbooksublist/',ebook.views.showbooksublist),
]
