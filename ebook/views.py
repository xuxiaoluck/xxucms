from django.http import HttpResponse
from django.shortcuts import render_to_response
from ebook.models import Publisher,BookType,Books,BookFiles

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
    #ablist = getallauthor(request)
    btblist = getallbooktype(request)

    return render_to_response('ebindex.html',locals())


'''
错误、无操作、增加出版社、作者、分类、书籍标题、图书列表都由一个页面完成，用一个变量来判断当前是哪个操作
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
    #ablist = getallauthor(request)
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

    pblist = getallpublisher(request)
    btblist = getallbooktype(request)
    return render_to_response('addbooks.html',locals())


def uploadfiles(request):
    '''上传图书附件，不会对原视图进行刷新'''
    return render_to_response('addbooks.html',locals())
    


