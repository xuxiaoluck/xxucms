from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import StreamingHttpResponse
from django.utils.http import urlquote
from datetime import datetime
import json,os

from ebook.models import Publisher,BookType,Books,BookFiles


def getallpublisher(request):
    '''取得所有出版社名称'''
    db = Publisher.objects.all()
    pblist = [one.name for one in db]
    return pblist

def getallbooktype(request):
    '''取得所有分类'''
    db = BookType.objects.all()
    btblist = [one.name for one in db]
    return btblist

def index(request):
    '''进行书籍首页'''
    dotype = 0 #无操作
    pblist = getallpublisher(request)
    btblist = getallbooktype(request)
    typelist = btblist[::2]
    typelist1 = btblist[1::2]
    return render_to_response('ebindex.html',locals())

def openaddbookandtype(request):
    '''打开新增界面'''

    if not request.user.is_authenticated:
        return render_to_response('nologin.html',locals())

    booktypelist = getallbooktype(request)
    publisherlist = getallpublisher(request)

    return render_to_response('addbooks.html',locals())


def addpublisher(request):
    '''增加出版社'''

    pname = request.POST.get('typename')
    info = ''
    if pname != '':
        try:
            tmpobj  = Publisher.objects.get(name = pname)
            info = '(<font color=red>{0}</font>)已存在!'.format(pname)
        except Publisher.DoesNotExist:
            db = Publisher(name = pname)
            info = '增加(<font color=red>{0}</font>)成功!'.format(pname)
            db.save()

    return HttpResponse(info)


def addbooktype(request):
    '''增加图书类别'''

    pname = request.POST.get('typename')
    info = ''
    if pname != '':
        try:
            tmpobj  = BookType.objects.get(name = pname)
            info = '(<font color=red>{0}</font>)已存在!'.format(pname)
        except BookType.DoesNotExist:
            db = BookType(name = pname)
            db.save()
            info = '增加(<font color=red>{0}</font>)成功!'.format(pname)
    return HttpResponse(info)


def addbooks(request):
    '''增加书籍'''

    bookid = request.POST['bookid']
    booktype = request.POST['booktype']
    bookname = request.POST['bookname']
    bookpublisher = request.POST['bookpublisher']
    bookauthors = request.POST['bookauthors']
    bookmemo = request.POST['bookmemo']
    booktypeobj = BookType.objects.get(name = booktype)
    publisherobj = Publisher.objects.get(name = bookpublisher)
    info = ''
    #print('BookID:',bookid,bookname)
    if booktype == '' or bookname == '' or bookpublisher == '' or bookauthors == '' or bookmemo == '':
        return HttpResponse(json.dumps({'retinfo':'<font color=red>数据不全！</font>','bookid':''}),content_type = 'application/json')

    if bookid == '': #新建
        bookobj = Books(name = bookname,
                          authors = bookauthors,
                          detial = bookmemo,
                          booktype = booktypeobj,
                          publisher = publisherobj,
                          updateuser = request.user.username
                          )
        bookobj.save()   #保存一项图书资源
        bookid = str(bookobj.id)
        info = '增加<font color=red>({0}</font>)成功!'.format(bookname)
    else: #修改
        modiobj = Books.objects.get(id = int(bookid))
        modiobj.name = bookname
        modiobj.authors = bookauthors
        modiobj.booktype = booktypeobj
        modiobj.publisher = publisherobj
        modiobj.detial = bookmemo
        modiobj.updateuser = request.user.username
        modiobj.updatetime = datetime.now()
        modiobj.save()
        info = '修改<font color=red>({0})</font>成功!'.format(bookname)

    return HttpResponse(json.dumps({'retinfo':info,'bookid':bookid}),content_type = 'application/json')

def uploadfiles(request):
    '''上传图书附件'''

    bookid = request.POST['bookid']
    fileobjs = request.FILES.getlist('files-my')
    if bookid == '':
        return HttpResponse('请先上传书籍资料！')
    else:
        for i in range(len(fileobjs)):
            #UploadFile objects
            oneobj = fileobjs[i]
            print('oneobj:',oneobj)
            if oneobj:  #得到上传的一个 file对象，可以直接保存到 FileField字段中
                booksobj = Books.objects.get(id = bookid)
                bookfile = BookFiles(name = oneobj.name,book_list = booksobj,uploadfile = oneobj)
                print('saveoneobj',booksobj,bookfile)
                bookfile.save()  #生成一条上传文件记录

        return HttpResponse(json.dumps('succ'),content_type = 'application/json')


def booklistbytypename(request):
    '''按类别名称列出一类书籍数据'''

    typename = request.GET.get('typename')
    booktype = BookType.objects.get(name = typename)
    booklist = booktype.books_set.all() #先得到外键对象，再找到外键的所有对象列表
    paginator = Paginator(booklist, 10) # 一页显示10条
    page = request.GET.get('page',1)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    bookrlt = [] #书籍列表
    for book in contacts:  #该页数据
        bookid = book.id
        bookname = book.name
        bookdetial = book.detial[:200]
        bookpublisher = book.publisher.name
        bookauthors = book.authors
        bookupdatetime = book.updatetime.strftime('%Y%m%d')
        bookfiles = book.bookfiles_set.all()  #得到所有附件
        filelist = []
        for onefile in bookfiles:
            tmpdict = {}
            tmpdict['name'] = onefile.name
            tmpdict['size'] = "{0:.2f}K".format(onefile.uploadfile.size / 1024.0)
            tmpdict['url'] = onefile.uploadfile.url
            tmpdict['fileid'] = onefile.id
            filelist.append(tmpdict)

        bookrlt.append({'bookid':bookid,'bookname':bookname,'bookdetial':book.detial,
                        'bookpublisher':bookpublisher,'bookauthors':bookauthors,'filelist':filelist})

    dotype = 0 #无操作
    pblist = getallpublisher(request)
    btblist = getallbooktype(request)
    typelist = btblist[::2]
    typelist1 = btblist[1::2]

    bookcount = len(bookrlt)
    pagenums = range(1,paginator.num_pages + 1)

    return render_to_response('ebindex.html',locals())


def downloadfile(request):
    '''下载文件到本地'''

    def file_iterator(file_name, chunk_size=1024):
        with open(file_name,'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    onefile = BookFiles.objects.get(id = request.GET.get('fileid'))
    the_file_name = onefile.uploadfile.path
    file_name = onefile.name
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(urlquote(file_name))

    return response

def modifybook(request):
    '''修改已上传的书籍资料'''
    bookid = request.GET['bookid']
    #得到一本书的内容，传到修改单元去。
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