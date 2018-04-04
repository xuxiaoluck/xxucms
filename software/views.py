"""
2018-04-03
徐潇
"""

from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import StreamingHttpResponse
from django.utils.http import urlquote
from datetime import datetime
import json,os

from software.models import SoftType,Softs,SoftFiles


def getallsofttype(request):
    '''取得所有软件类别'''
    db = SoftType.objects.all()
    stlist = [one.name for one in db]
    return stlist


def index(request):
    '''软件首页'''

    stlist = getallsofttype(request)
    typelist = stlist[::2]
    typelist1 = stlist[1::2]
    return render_to_response('software.html',locals())

def openaddsoftandtype(request):
    '''打开新增界面'''

    if not request.user.is_authenticated:
        return render_to_response('nologin.html',locals())

    softtypelist = getallsofttype(request)

    return render_to_response('addsoft.html',locals())


def addsofttype(request):
    '''增加类别'''

    pname = request.POST.get('typename')
    info = ''
    newflag = False
    if pname != '':
        try:
            tmpobj  = SoftType.objects.get(name = pname)
            info = '(<font color=red>{0}</font>)已存在!'.format(pname)
        except SoftType.DoesNotExist:
            db = SoftType(name = pname)
            db.save()
            info = '增加(<font color=red>{0}</font>)成功!'.format(pname)
            newflag = True

    return HttpResponse(json.dumps({'info':info,'newflag':newflag}),content_type = 'application/json')


def addsoft(request):
    '''增加软件'''

    softid = request.POST['softid']
    softtype = request.POST['softtype']
    softname = request.POST['softname']
    softmemo = request.POST['softmemo']
    softtypeobj = SoftType.objects.get(name = softtype)
    info = ''

    #判断是否有效放JS前端
    #if softtype == '' or softname == '' or softmemo == '':
    #    return HttpResponse(json.dumps({'retinfo':'<font color=red>数据不全！</font>','softid':''}),content_type = 'application/json')

    if softid == '': #新建
        softobj = Softs(name = softname,
                          detial = softmemo,
                          softtype = softtypeobj,
                          updateuser = request.user.username
                          )
        softobj.save()   #保存一项图书资源
        softid = str(softobj.id)
        info = '增加<font color=red>({0}</font>)成功!'.format(softname)
    else: #修改
        modiobj = Softs.objects.get(id = int(softid))
        modiobj.name = softname
        modiobj.softtype = softtypeobj
        modiobj.detial = softmemo
        modiobj.updateuser = request.user.username
        modiobj.updatetime = datetime.now()
        modiobj.save()
        info = '修改<font color=red>({0})</font>成功!'.format(bookname)

    return HttpResponse(json.dumps({'retinfo':info,'softid':softid}),content_type = 'application/json')

def uploadfiles(request):
    '''上传软件附件'''

    softid = request.POST['softid']
    fileobjs = request.FILES.getlist('files-my')
    if softid == '':
        return HttpResponse('请先增加软件资料！')
    else:
        for i in range(len(fileobjs)):
            #UploadFile objects
            oneobj = fileobjs[i]
            if oneobj:  #得到上传的一个 file对象，可以直接保存到 FileField字段中
                softobj = Softs.objects.get(id = softid)
                softfileobj = SoftFiles(name = oneobj.name,soft_list = softobj,uploadfile = oneobj)
                softfileobj.save()  #生成一条上传文件记录

        return HttpResponse(json.dumps('succ'),content_type = 'application/json')


def softlistbytypename(request):
    '''按类别名称列出一类软件'''

    typename = request.GET.get('typename')
    softtypeobj = SoftType.objects.get(name = typename)
    softlistobj = softtypeobj.softs_set.all() #先得到外键对象，再找到外键的所有对象列表
    paginator = Paginator(softlistobj, 10) # 一页显示10条
    page = request.GET.get('page',1)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    softrlt = [] #软件文件列表
    for soft in contacts:  #该页数据
        softid = soft.id
        softname = soft.name
        softdetial = soft.detial[:200]
        softupdatetime = soft.updatetime.strftime('%Y%m%d')
        softfileobj = soft.softfiles_set.all()  #得到所有附件
        filelist = []
        for onefile in softfileobj:
            tmpdict = {}
            tmpdict['name'] = onefile.name
            tmpdict['size'] = "{0:.2f}K".format(onefile.uploadfile.size / 1024.0)
            #tmpdict['url'] = onefile.uploadfile.url
            tmpdict['fileid'] = onefile.id
            filelist.append(tmpdict)

        softrlt.append({'softid':softid,'softname':softname,'softdetial':soft.detial,'filelist':filelist})

    btlist = getallsofttype(request)
    typelist = btlist[::2]
    typelist1 = btlist[1::2]

    softcount = len(softrlt)
    pagenums = range(1,paginator.num_pages + 1)

    return render_to_response('software.html',{'softrlt':softrlt,'typelist':typelist,'typelist1':typelist1})


def downloadsoft(request):
    '''下载文件到本地'''

    def file_iterator(file_name, chunk_size=1024):
        with open(file_name,'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    onefile = SoftFiles.objects.get(id = request.GET.get('fileid'))
    the_file_name = onefile.uploadfile.path
    file_name = onefile.name
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(urlquote(file_name))

    return response

def modifybook(request):
    '''修改'''
    return
    softid = request.GET['softid']

    bookdict = {}
    bookdict['bookid'] = bookid
    bookobj = Books.objects.get(id = bookid)
    bookdict['bookname'] = bookobj.name
    bookdict['booktype'] = bookobj.booktype.name
    bookdict['bookpublisher'] = bookobj.publisher.name
    bookdict['bookauthors'] = bookobj.authors
    bookdict['bookdetial'] = bookobj.detial


    #下面得到书籍的附件列表，每条为一个字典
    filelist = []
    fileobjs = bookobj.bookfiles_set.all()
    for onefile in fileobjs:
        #一条文件信息，id 名称 路径 大小（K） 路径
        tmpdict = {}
        tmpdict['fileid'] = onefile.id
        tmpdict['filename'] = onefile.name
        #tmpdict['filepath'] = onefile.uploadfile.path
        tmpdict['filesize'] = "{0:.2f}K".format(onefile.uploadfile.size / 1024.0)
        filelist.append(tmpdict)


    booktypelist = getallbooktype(request)
    publisherlist = getallpublisher(request)

    return render_to_response('modifybook.html',{'bookdict':json.dumps(bookdict),'filelist':filelist,
                                                 'booktypelist':booktypelist,'publisherlist':publisherlist})

def deleteonebookfile(request):
    '''删除一本书资料的一个附件文件即实际的书籍'''

    fileid = request.POST['fileid']

    fileobj = BookFiles.objects.get(id = fileid)
    filepath = fileobj.uploadfile.path
    #得到文件对象及文件对象的实际路径
    name = fileobj.name
    fileobj.delete()
    os.remove(filepath)
    return HttpResponse('delete onefile [{0}] OK!'.format(name))


def deleteonebook(request):
    '''删除一本书籍所有信息'''
    bookid = request.POST['bookid']
    bookobj = Books.objects.get(id = bookid)
    bookfilesobj = bookobj.bookfiles_set.all()
    #print(bookfilesobj[0].name)
    name = bookobj.name
    for onefileobj in bookfilesobj:
        os.remove(onefileobj.uploadfile.path)
        print("remove")
        #删除实际文件
    bookobj.delete()
    #删除books中的信息时自动删除关联它的外建的表
    return HttpResponse('delete book [{0}] OK!'.format(name))



