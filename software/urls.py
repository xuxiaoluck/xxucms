"""  URL Configuration
软件下载URL转发配置
"""

from django.urls import path,include
from software.views import *

urlpatterns = [
    path('',index), #首页
    path('software/',index),
    path('openaddsoftandtype/',openaddsoftandtype),
    path('addsofttype/',addsofttype),
    path('addsoft/',addsoft),
    path('uploadfiles/',uploadfiles),
    path('softlistbytypename/',softlistbytypename),
    path('downloadsoft/',downloadsoft),
]
