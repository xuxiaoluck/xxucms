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
    #softtypeobj = SoftType.objects.get(name = softtype)
    info = ''

    #判断是否有效放JS前端
    #if softtype == '' or softname == '' or softmemo == '':
    #    return HttpResponse(json.dumps({'retinfo':'<font color=red>数据不全！</font>','softid':''}),content_type = 'application/json')

    if softid == '': #新建
        softobj = Softs(name = softname,
                          detial = softmemo,
                          softtypes = softtype,
                          updateuser = request.user.username
                          )
        softobj.save()   #保存一项图书资源
        softid = str(softobj.id)
        info = '增加<font color=red>({0}</font>)成功!'.format(softname)
    else: #修改
        modiobj = Softs.objects.get(id = int(softid))
        modiobj.name = softname
        modiobj.softtypes = softtype
        modiobj.detial = softmemo
        modiobj.updateuser = request.user.username
        modiobj.updatetime = datetime.now()
        modiobj.save()
        info = '修改<font color=red>({0})</font>成功!'.format(softname)

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
    softlistobj = Softs.objects.filter(softtypes__contains = typename)
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

    return render_to_response('software.html',{'softrlt':softrlt,'typelist':typelist,'typelist1':typelist1,'request':request})


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

    onefile.accessnums += 1
    onefile.save()
    softobj = onefile.soft_list
    softobj.accessnums += 1
    softobj.save()  #更新访问列表

    the_file_name = onefile.uploadfile.path
    file_name = onefile.name
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(urlquote(file_name))

    return response

def modifysoft(request):
    '''修改'''

    softid = request.GET['softid']
    softdict = {}
    softdict['softid'] = softid
    softobj = Softs.objects.get(id = softid)
    softobj.accessnums += 1
    softobj.save()

    softdict['softname'] = softobj.name
    #softdict['softtype'] = softobj.softtype.name
    softdict['softdetial'] = softobj.detial

    existsofttypes = softobj.softtypes.split('||') 
    #下面得到软件的附件列表，每条为一个字典
    filelist = []
    fileobjs = softobj.softfiles_set.all()
    for onefile in fileobjs:
        #一条文件信息，id 名称 路径 大小（K） 路径
        tmpdict = {}
        tmpdict['fileid'] = onefile.id
        tmpdict['filename'] = onefile.name
        tmpdict['filesize'] = "{0:.2f}K".format(onefile.uploadfile.size / 1024.0)
        filelist.append(tmpdict)


    softtypelist = getallsofttype(request)

    return render_to_response('modifysoft.html',{'softdict':json.dumps(softdict),'filelist':filelist,
                                                 'softtypelist':softtypelist,'existsofttypes':existsofttypes})

def deleteonesoftfile(request):
    '''删除一项软件书资料的一个附件文件即实际的一个软件'''

    fileid = request.POST['fileid']

    fileobj = SoftFiles.objects.get(id = fileid)
    filepath = fileobj.uploadfile.path
    #得到文件对象及文件对象的实际路径
    name = fileobj.name
    fileobj.delete()
    os.remove(filepath)
    return HttpResponse('delete onefile [{0}] OK!'.format(name))


def deleteonesoft(request):
    '''删除一项软件所有信息'''
    softid = request.POST['softid']
    softobj = Softs.objects.get(id = softid)
    softfilesobj = softobj.softfiles_set.all()
    name = softobj.name
    for onefileobj in softfilesobj:
        os.remove(onefileobj.uploadfile.path)
        #删除实际文件
    softobj.delete()
    #删除softs中的信息时自动删除关联它的外建的表
    return HttpResponse('delete soft [{0}] OK!'.format(name))



