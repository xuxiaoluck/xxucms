from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from ebook.models import Publisher,BookType,Books,BookFiles
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import StreamingHttpResponse
from django.utils.http import urlquote

def getallpublisher(request):
    '''取得所有出版社名称'''
    db = Publisher.objects.all()
    pblist = [one.name for one in db]
    return pblist

"""

def getallauthor(request):
    '''取得所有作者名称'''
    db = Author.objects.all()
    ablist = [one.name for one in db]
    return ablist
"""

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


'''
错误-1、无操作0、增加出版社1、作者2、分类3、图书资源4、图书列表5都由一个页面完成，用一个变量来判断当前是哪个操作
dotype:-1,0,1,2,3,4
dotype:-100,数据已存在
'''
def addpublisher(request):
    '''增加出版社'''
    dotype = -1
    isaddpublisher = True
    if request.method == 'POST':
        pname = request.POST.get('addpublishername','')
        if pname != '':
            try:
                tmpobj  = Publisher.objects.get(name = pname)
                dotype = -100 #无异常，说明已存在
            except Publisher.DoesNotExist:
                db = Publisher(name = pname)
                db.save()
                dotype = 1

    pblist = getallpublisher(request)
    btblist = getallbooktype(request)

    return render_to_response('addbooks.html',locals())

def addauthor(request):
    '''增加作者'''
    dotype = -1
    isaddauthor = True
    if request.method == 'POST':
        pname = request.POST.get('addauthorname','')
        if pname != '':
            try:
                tmpobj  = Author.objects.get(name = pname)
                dotype = -100 #无异常，说明已存在
            except Author.DoesNotExist:
                db = Author(name = pname)
                db.save()
                dotype = 2

    pblist = getallpublisher(request)
    btblist = getallbooktype(request)
    return render_to_response('addbooks.html',locals())


def addbooktype(request):
    '''增加图书类别'''
    dotype = -1
    isaddbooktype = True
    if request.method == 'POST':
        pname = request.POST.get('addbooktypename','')
        if pname != '':
            try:
                tmpobj  = BookType.objects.get(name = pname)
                dotype = -100 #无异常，说明已存在
            except BookType.DoesNotExist:
                db = BookType(name = pname)
                db.save()
                dotype = 3
    pblist = getallpublisher(request)
    btblist = getallbooktype(request)
    return render_to_response('addbooks.html',locals())

def addbooks(request):
    '''增加书籍'''

    if not request.user.is_authenticated:
        return render_to_response('nologin.html',locals())

    #先判断是否已登录，非登录用户不能增加数据

    pblist = getallpublisher(request)
    btblist = getallbooktype(request)
    dotype = -1
    isaddbook = True
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
            modiobj.save()
            bookid = modiobj.id
        else:
            bookobj = Books(name = bookname,
                          authors = bookauthors,
                          detial = detial,
                          booktype = booktypeid,
                          publisher = publisherid
                          )
            bookobj.save()   #保存一项图书资源
            bookid = bookobj.id  #得到最新的BOOKiD
        dotype = 4
    return render_to_response('addbooks.html',locals())


def uploadfiles(request):
    '''上传图书附件'''

    if request.method == 'POST':
        bookid = int(request.POST.get('bookid',0))
        fileobjs = request.FILES.getlist('files-my')
        for i in range(len(fileobjs)):
            #UploadFile objects
            oneobj = fileobjs[i]
            if oneobj:  #得到上传的一个 file对象，可以直接保存到 FileField字段中
                booksid = Books.objects.get(id = bookid)
                bookfile = BookFiles(name = oneobj.name,book_list = booksid,uploadfile = oneobj)
                bookfile.save()  #生成一条上传文件记录

        bookobj = Books.objects.get(id = bookid)
        booktypename = bookobj.booktype.name
        publishername = bookobj.publisher.name
        bookname = bookobj.name
        detial = bookobj.detial
        bookauthors = bookobj.authors
        dotype = 4
        isaddbook = True

    return render_to_response('addbooks.html',locals())



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
        bookdetial = book.detial[:50]
        bookpublisher = book.publisher.name
        bookauthors = book.authors
        bookfiles = book.bookfiles_set.all()  #得到所有附件
        filelist = []
        for onefile in bookfiles:
            tmpdict = {}
            tmpdict['name'] = onefile.name
            tmpdict['uploaddate'] = onefile.uploadtime.strftime('%Y%m%d')
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
