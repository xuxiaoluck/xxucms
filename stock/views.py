from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import StreamingHttpResponse
from django.utils.http import urlquote
from datetime import datetime
import json

#2018-04-08

from stock.models import *
import tushare as ts

def index(request):
    '''打开首页'''
    return render_to_response('stock.html',locals())



def update_industry(request):
    '''更新行业数据'''
    industryobj = stock_industry.objects.all()
    industryobj.delete()

    rltobj = ts.get_industry_classified()
    objlist = []
    for item in rltobj:
        tmpobj = stock_industry(code = item.code,name = item.name,i_name = item.c_name)
        objlist.append(tmpobj)

    industryobj.objects.bulk_create(objlist)

    return HttpResponse('succ.{0}条!'.format(len(objlist)))

