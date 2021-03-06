"""cost  URL Configuration
money
"""

from django.urls import path,include
import cost.views

urlpatterns = [
    path('xxucost123456789/',cost.views.index), #首页
    path('getcostinfo/',cost.views.getcostinfo), #得到COST信息，在首页上显示相关信息
    path('openinputcost/',cost.views.openinputcost),
    path('addonecost/',cost.views.addonecost),
    path('addonetype/',cost.views.addonetype),
    path('addonesubject/',cost.views.addonesubject),
    path('opentotalcost/',cost.views.opentotalcost),
    path('totalcost/',cost.views.totalcost),
]
