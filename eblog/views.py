from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import StreamingHttpResponse
from django.utils.http import urlquote
from datetime import datetime
import json

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

    if not request.user.is_authenticated:
        return render_to_response('nologin.html',locals())

    btlist = getallblogtype(request)
    return render_to_response('addblogandtype.html',locals())

def addblogtype(request):
    '''增加类别,通过jquery.post传递数据'''

    typename = request.POST.get('typename')

    retinfo = ''
    retflag = False
    if typename != '':
        try:
            tmpobj  = BlogType.objects.get(name = typename)
            #无异常，说明已存在
            retinfo =  '(<font color=red>{0}</font>)已存在!'.format(typename)
        except BlogType.DoesNotExist:
                db = BlogType(name = typename)
                db.save()
                retinfo = '(<font color=red>{0}</font>)成功!'.format(typename)
                retflag = True
    else:
                retinfo = '(<font color=red>{0}</font>)'.format('名称不能为空')

    return HttpResponse(json.dumps({'retflag':retflag,'retinfo':retinfo}),content_type='application/json')

def saveblog(request):
    '''增加、修改博文'''

    #后端默认使用 POST传输
    '''数据库字段：
    name,blogtype,detial,authors,accessnums,thumbnums,updatetime  后三个有默认值
    '''
    typename = request.POST['blogtypename']
    blogname = request.POST.get('blogname')
    blogmemo = request.POST.get('blogmemo')
    #print(typename,blogname,blogmemo)
    if typename == '' or blogname == '' or blogmemo == '':
        return HttpResponse('增加文章:<font color=red>标题、类别、内容不能为空!</font>')

    blogtypeobj = BlogType.objects.get(name = typename)  #得到类型的外键对象
    retid = request.POST['blogid']
    retinfo = '增加文章<font color=red>[{0}]</font>成功!'.format(typename)

    if retid == '':
        ##新建
        blogobj = Blogs(name = blogname,
                          detial = blogmemo,
                          blogtype = blogtypeobj,
                          authors = request.user.username
                          )
        blogobj.save()
        retid = blogobj.id
    else:
        #修改 只更新标题、内容、类别三个字段，其它暂未考虑
        blogobj = Blogs.objects.get(id = int(request.POST['blogid']))
        blogobj.name = blogname
        blogobj.detial = blogmemo
        blogobj.blogtype = blogtypeobj
        blogobj.save()
        retinfo = '修改文章<font color=red>[{0}]</font>成功!'.format(typename)

    return HttpResponse(json.dumps({'retinfo':retinfo,'retid':retid}),content_type = 'application/json')



