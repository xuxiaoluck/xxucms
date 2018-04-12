"""stock  URL Configuration

"""

from django.urls import path,include
from stock.views import *

urlpatterns = [
    path('',index), #首页
    path('updateindustry/',update_industry),
]
