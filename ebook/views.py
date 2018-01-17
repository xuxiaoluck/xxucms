from django.http import HttpResponse
from django.shortcuts import render_to_response
from ebook.models import Publisher

def getallpublisher(request):
    '''取得所有出版社名称和ID'''
    db = Publisher.objects.all() 
    pblist = []
    for db_one in db:
        pblist.append((db_one.id,db_one.name)) #列表项一个元组(id,name)
    return pblist

def index(request):
    '''进行书籍首页'''
    dotype = 0 #无操作
    pblist = getallpublisher(request)
    
    return render_to_response('ebindex.html',locals())


'''
错误、无操作、增加出版社、作者、分类、书籍标题、图书列表都由一个页面完成，用一个变量来判断当前是哪个操作
dotype:-1,0,1,2,3,4
'''

def addpublisher(request):
    '''增加出版社'''
    dotype = -1
    if request.method == 'POST':
        pname = request.POST.get('addpublishername','')
        if pname != '':
           db = Publisher(name = pname)
           db.save()
           dotype = 1

    testval = request.POST.getlist('publisherlist1')
    pblist =  getallpublisher(request)
    return render_to_response('addbooks.html',locals())

def addbooks(request):
    '''增加书籍'''
    pblist = getallpublisher(request)
    return render_to_response('addbooks.html',locals())





