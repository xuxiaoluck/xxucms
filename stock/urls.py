"""stock  URL Configuration

"""

from django.urls import path,include
from stock.views import *

urlpatterns = [
    path('',index), #首页
    path('updateindustry/',update_industry),
    path('updateconcept/',update_concept),
    path('updatearea/',update_area),
    path('updatehs300/',update_hs300),
    path('updatesz50/',update_sz50),
    path('updatezz500/',update_zz500),
    path('updateterminate/',update_terminate),
    path('updatesuspend/',update_suspend),
    path('updategem/',update_gem), #创业板
    path('updatesme/',update_sme), #中小板
    path('updatest/',update_st),
    path('data_mgr/',datamgr),  #数据管理
    path('type_info/',typeinfo), #打开行业数据
    path('getindustryinfo/',getindustryinfo),#显示行业数据
    path('getareainfo/',getareainfo),
    path('getconceptinfo/',getconceptinfo),
    path('getstinfo/',getstinfo),
    path('getgeminfo/',getgeminfo),
    path('getsmeinfo/',getsmeinfo),
    path('getzz500info/',getzz500info),
    path('getsz50info/',getsz50info),
    path('geths300info/',geths300info),
    path('getterminateinfo/',getterminateinfo),
    path('getsuspendinfo/',getsuspendinfo),
]
