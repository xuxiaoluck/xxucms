from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import StreamingHttpResponse
from django.utils.http import urlquote
from datetime import datetime
from eblog.models import BlogType,Blogs,BlogFiles,BlogImages


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


def addblogtype(request):
    '''增加类别'''

    if request.method == 'POST':
        pname = request.POST.get('blogtypename','')
        if pname != '':
            try:
                tmpobj  = BlogType.objects.get(name = pname)
                #无异常，说明已存在
            except BlogType.DoesNotExist:
                db = BlogType(name = pname)
                db.save()

    btlist = getallblogtype(request)
    return render_to_response('addblogandtype.html',locals())

def addblogandtype(request):
    '''增加'''
    return render_to_response('addblogandtype.html',locals())

def addblog(request):
    '''增加博文'''

    if not request.user.is_authenticated:
        return render_to_response('nologin.html',locals())

    #先判断是否已登录，非登录用户不能增加数据

    pblist = getallpublisher(request)
    btblist = getallbooktype(request)

    if request.method == 'POST':
        booktype = request.POST.get('addbookselecttype')
        publisher = request.POST.get('addbookselectpublisher')
        booktypeid = BookType.objects.get(name = booktype)
        publisherid = Publisher.objects.get(name = publisher)  #得到外键对象
        publishername = publisherid.name
        booktypename = booktypeid.name #传回到页面中
        bookname = request.POST.get('addbookname')
        detial = request.POST.get('addbookmemo')
        bookauthors = request.POST.get('addbookauthor')
        checkboxstate = request.POST.get('modifydata','NO')
        if checkboxstate == 'OK': #修改
            modiobj = Books.objects.get(id = int(request.POST.get('addbookid')))
            modiobj.name = bookname
            modiobj.authors = bookauthors
            modiobj.booktype = booktypeid
            modiobj.publisher = publisherid
            modiobj.detial = detial
            modiobj.updateuser = request.user.username
            modiobj.updatetime = datetime.now()
            modiobj.save()
            bookid = modiobj.id
        else:
            bookobj = Books(name = bookname,
                          authors = bookauthors,
                          detial = detial,
                          booktype = booktypeid,
                          publisher = publisherid,
                          updateuser = request.user.username
                          )
            bookobj.save()   #保存一项图书资源
            bookid = bookobj.id  #得到最新的BOOKiD
        dotype = 4
    return render_to_response('addblogandtype.html',locals())

