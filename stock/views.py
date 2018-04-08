from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import StreamingHttpResponse
from django.utils.http import urlquote
from datetime import datetime
import json

#2018-04-08

def index(request):
    '''打开首页'''
    return render_to_response('stock.html',locals())


