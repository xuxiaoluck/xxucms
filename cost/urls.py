"""cost  URL Configuration
money
"""

from django.urls import path,include
import cost.views

urlpatterns = [
    path('xxucost123456789/',cost.views.index), #首页
]
