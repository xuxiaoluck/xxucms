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


def datamgr(request):
    '''打开管理数据页面'''
    '''if not request.user.is_authenticated:
        return render_to_response('nologin.html',locals())
    '''
    return render_to_response('stockdatamgr.html',{'request':request,'islogin':request.user.is_authenticated})

def typeinfo(request):
    '''打开分类页面'''
    return render_to_response('stocktypeinfo.html',{'request':request,'islogin':request.user.is_authenticated})



def update_industry(request):
    '''更新行业数据'''
    industryobj = stock_industry.objects.all()
    industryobj.delete()

    rltobj = ts.get_industry_classified()
    objlist = []
    for i in range(len(rltobj)):
        tmpobj = stock_industry(code = rltobj.loc[i]['code'],name = rltobj.loc[i]['name'],i_name = rltobj.loc[i]['c_name'])
        objlist.append(tmpobj)

    stock_industry.objects.bulk_create(objlist)

    return HttpResponse('succ.{0}条!'.format(len(objlist)))

def update_concept(request):
    '''更新概念数据'''
    conceptobj = stock_concept.objects.all()
    conceptobj.delete()

    rltobj = ts.get_concept_classified()
    objlist = []
    for i in range(len(rltobj)):
        tmpobj = stock_concept(code = rltobj.loc[i]['code'],name = rltobj.loc[i]['name'],c_name = rltobj.loc[i]['c_name'])
        objlist.append(tmpobj)

    stock_concept.objects.bulk_create(objlist)

    return HttpResponse('succ.{0}条!'.format(len(objlist)))

def update_area(request):
    '''更新地域数据'''
    stock_area.objects.all().delete()

    rltobj = ts.get_area_classified()
    objlist = []
    for i in range(len(rltobj)):
        tmpobj = stock_area(code = rltobj.loc[i]['code'],name = rltobj.loc[i]['name'],a_name = rltobj.loc[i]['area'])
        objlist.append(tmpobj)

    stock_area.objects.bulk_create(objlist)

    return HttpResponse('succ.{0}条!'.format(len(objlist)))

def update_sme(request):
    '''更新中小板数据'''
    stock_sme.objects.all().delete()

    rltobj = ts.get_sme_classified()
    objlist = []
    for i in range(len(rltobj)):
        tmpobj = stock_sme(code = rltobj.loc[i]['code'],name = rltobj.loc[i]['name'])
        objlist.append(tmpobj)

    stock_sme.objects.bulk_create(objlist)

    return HttpResponse('succ.{0}条!'.format(len(objlist)))

def update_gem(request):
    '''更新创业板'''
    stock_gem.objects.all().delete()

    rltobj = ts.get_gem_classified()
    objlist = []
    for i in range(len(rltobj)):
        tmpobj = stock_gem(code = rltobj.loc[i]['code'],name = rltobj.loc[i]['name'])
        objlist.append(tmpobj)

    stock_gem.objects.bulk_create(objlist)

    return HttpResponse('succ.{0}条!'.format(len(objlist)))

def update_st(request):
    '''更新st板块'''
    stock_st.objects.all().delete()

    rltobj = ts.get_st_classified()
    objlist = []
    for i in range(len(rltobj)):
        tmpobj = stock_st(code = rltobj.loc[i]['code'],name = rltobj.loc[i]['name'])
        objlist.append(tmpobj)

    stock_st.objects.bulk_create(objlist)

    return HttpResponse('succ.{0}条!'.format(len(objlist)))

def update_hs300(request):
    '''更新沪深300'''
    stock_hs300.objects.all().delete()

    rltobj = ts.get_hs300s()
    objlist = []
    for i in range(len(rltobj)):
        tmpobj = stock_hs300(code = rltobj.loc[i]['code'],name = rltobj.loc[i]['name'],date = rltobj.loc[i]['date'],weight = rltobj.loc[i]['weight'])
        objlist.append(tmpobj)

    stock_hs300.objects.bulk_create(objlist)

    return HttpResponse('succ.{0}条!'.format(len(objlist)))


def update_sz50(request):
    '''更新上证50'''
    stock_sz50.objects.all().delete()

    rltobj = ts.get_sz50s()
    objlist = []
    for i in range(len(rltobj)):
        tmpobj = stock_sz50(code = rltobj.loc[i]['code'],name = rltobj.loc[i]['name'])
        objlist.append(tmpobj)

    stock_sz50.objects.bulk_create(objlist)

    return HttpResponse('succ.{0}条!'.format(len(objlist)))

def update_zz500(request):
    '''更新中证500'''
    stock_zz500.objects.all().delete()

    rltobj = ts.get_zz500s()
    objlist = []
    for i in range(len(rltobj)):
        tmpobj = stock_zz500(code = rltobj.loc[i]['code'],name = rltobj.loc[i]['name'])
        objlist.append(tmpobj)

    stock_zz500.objects.bulk_create(objlist)

    return HttpResponse('succ.{0}条!'.format(len(objlist)))

def update_terminate(request):
    '''更新终止上市'''
    stock_terminate.objects.all().delete()

    rltobj = ts.get_terminated()
    objlist = []
    for i in range(len(rltobj)):
        tmpobj = stock_terminate(code = rltobj.loc[i]['code'],name = rltobj.loc[i]['name'],
                                 #s_date = datetime.strptime(rltobj.loc[i]['oDate'],'%Y-%m-%d'),
                                 #e_date = datetime.strptime(rltobj.loc[i]['tDate'],'%Y-%m-%d'))
                                 s_date = rltobj.loc[i]['oDate'],
                                 e_date = rltobj.loc[i]['tDate'])
        objlist.append(tmpobj)

    stock_terminate.objects.bulk_create(objlist)

    return HttpResponse('succ.{0}条!'.format(len(objlist)))


def update_suspend(request):
    '''更新暂停上市'''
    stock_suspend.objects.all().delete()

    rltobj = ts.get_suspended()
    objlist = []
    for i in range(len(rltobj)):
        tmpobj = stock_suspend(code = rltobj.loc[i]['code'],name = rltobj.loc[i]['name'],
                                s_date = rltobj.loc[i]['oDate'],
                                e_date = rltobj.loc[i]['tDate'])
        objlist.append(tmpobj)

    stock_suspend.objects.bulk_create(objlist)

    return HttpResponse('succ.{0}条!'.format(len(objlist)))

''' 取得数据字段说明
code,代码,name,名称,industry,所属行业,area,地区,pe,市盈率,outstanding,流通股本(亿),totals,总股本(亿),totalAssets,总资产(万),liquidAssets,流动资产,fixedAssets,固定资产,
reserved,公积金,reservedPerShare,每股公积金,esp,每股收益,bvps,每股净资,pb,市净率,timeToMarket,上市日期,undp,未分利润,perundp, 每股未分配,rev,收入同比(%),profit,利润同比(%),gpr,毛利率(%),
npr,净利润率(%),holders,股东人数
'''
def update_basics(request):
    '''更新股票基本资料'''



def gettypeinfo(request):
    '''显示股票分类'''
    return HttpResponse('[2900]')









