"""cost  URL Configuration
money
"""

from django.urls import path,include
import cost.views

urlpatterns = [
    path('',cost.views.index), #首页
]
