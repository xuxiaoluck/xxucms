from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import StreamingHttpResponse
from django.utils.http import urlquote
from datetime import datetime
import json,os

from cost.models import CostType,CostSubject,Money

'''2018-06-14
'''


def index(request):
    '''首页'''

    #先验证是否登录
    if not request.user.is_authenticated:
        return render_to_response('nologin.html',locals())

    typelist = list(CostType.objects.all().values())  #得到所有类型列表，每条为一个字典,KEY为字段名
    subjectlist = list(CostSubject.objects.all().values().order_by('name'))
    yearlist = Money.objects.values('year').order_by('-year').distinct()
    monthlist = range(1,13)
    return render_to_response('cost.html',locals())





