from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import StreamingHttpResponse
from django.utils.http import urlquote
from datetime import datetime

from eblog.models import BlogType,Blogs


def getallblogtype(request):
    '''取得所有分类'''
    db = BlogType.objects.all()
    btblist = [one.name for one in db]
    return btblist

def index(request):
    '''首页'''

    btblist = getallblogtype(request)
    typelist = btblist[::2]
    typelist1 = btblist[1::2] #分奇偶得到两个列表
    return render_to_response('blogindex.html',locals())

def openaddblogandtype(request):
    '''打开增加类别、博文的页面'''

    btlist = getallblogtype(request)
    return render_to_response('addblogandtype.html',locals())

def addblogtype(request):
    '''增加类别,通过jquery.post传递数据'''

    typename = request.POST.get('typename')

    if typename != '':
        try:
            tmpobj  = BlogType.objects.get(name = typename)
            #无异常，说明已存在
            return HttpResponse('(<font color=red>{0}</font>)已存在!'.format(typename))
        except BlogType.DoesNotExist:
                db = BlogType(name = typename)
                db.save()
                return HttpResponse('(<font color=red>{0}</font>)成功!'.format(typename))
    else:
                return HttpResponse('(<font color=red>{0}</font>)'.format('名称不能为空'))

def saveblog(request):
    '''增加、修改博文'''

#    if not request.user.is_authenticated:
#        return render_to_response('nologin.html',locals())

    #先判断是否已登录，非登录用户不能增加数据
    if request.method == 'POST':
        typename = request.POST['blogtypename']
        blogname = request.POST.get('blogname')
        blogmemo = request.POST.get('blogmemo')
        print(typename,blogname,blogmemo)

    return HttpResponse("succ")



