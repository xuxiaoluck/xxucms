from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib import auth
#from django.template.context_processors import csrf
from django.template import RequestContext
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from ebook.models import Books,BookFiles
from eblog.models import Blogs
from software.models import Softs
import json



def test(request):
    '''测试视图'''

    return render_to_response('test.html',locals())

def index(request):
    """主页,显示最新上传的五个软件、文章、图书"""

    bookn = Books.objects.order_by('-updatetime')[:5]  #按更新时间取最新的五条图书数据
    bookrlt = [] #书籍列表
    for book in bookn:  #附件生成下拦菜单
        bookid = book.id
        bookname = book.name
        bookdetial = book.detial[:200]
        bookpublisher = book.publisher.name
        bookauthors = book.authors
        bookupdatetime = book.updatetime.strftime('%Y-%m-%d %H:%M:%S')
        bookaccessnums = book.accessnums
        bookfiles = book.bookfiles_set.all()  #得到所有附件
        filelist = []
        for onefile in bookfiles:
            tmpdict = {}
            tmpdict['name'] = onefile.name
            tmpdict['size'] = "{0:.2f}K".format(onefile.uploadfile.size / 1024.0)
            tmpdict['url'] = onefile.uploadfile.url
            tmpdict['fileid'] = onefile.id
            filelist.append(tmpdict)

        bookrlt.append({'bookid':bookid,'bookname':bookname,'bookdetial':book.detial,'updatetime':bookupdatetime,'accessnums':bookaccessnums,
                        'bookpublisher':bookpublisher,'bookauthors':bookauthors,'filelist':filelist})


    #取前5个最新软件
    softn = Softs.objects.order_by('-updatetime')[:5]  #按更新时间取最新的五条
    softrlt = []
    for soft in softn:  #附件生成下拦菜单
        softid = soft.id
        softname = soft.name
        softdetial = soft.detial[:200]
        softupdatetime = soft.updatetime.strftime('%Y-%m-%d %H:%M:%S')
        softaccessnums = soft.accessnums
        softfiles = soft.softfiles_set.all()  #得到所有附件
        filelist = []
        for onefile in softfiles:
            tmpdict = {}
            tmpdict['name'] = onefile.name
            tmpdict['size'] = "{0:.2f}K".format(onefile.uploadfile.size / 1024.0)
            tmpdict['fileid'] = onefile.id
            filelist.append(tmpdict)

        softrlt.append({'softid':softid,'softname':softname,'softdetial':soft.detial,'updatetime':softupdatetime,'accessnums':softaccessnums,
                        'filelist':filelist})

    #下面取最新的10篇博客文章
    blogn = Blogs.objects.order_by('-updatetime')[:10]
    blogrlt = []
    for blog in blogn:
        blogid = blog.id
        blogname = blog.name
        blogrlt.append({'blogid':blogid,'blogname':blogname})

    return render_to_response('index.html',{'bookrlt':bookrlt,'blogrlt':blogrlt,'softrlt':softrlt,'request':request})

def nologin(request):
    '''打开未登录界面'''
    return render_to_response('nologin.html',locals())

def xlogin(request):
    '''登录视图'''

    uid = request.POST.get('uid','')
    pwd = request.POST.get('pwd','')
    user = auth.authenticate(username = uid,password = pwd)

    if user is not None and user.is_active:
        auth.login(request,user)
        print('login')
    else:
        print('nologin')

    return HttpResponseRedirect("/home/")


def xlogout(request):
    auth.logout(request)
    return render_to_response('index.html',locals())


def userreg(request):
    '''点击了用户注册后的视图'''
    return render_to_response('userreg.html',{'regsave':False,'regok':False})

def regsave(request):
    '''保存注册信息视图,regsave 判断是否启动一次注册过程，regok判断是否注册成功'''

    uid = request.POST.get('username','')
    pwd = request.POST.get('password','')
    if uid == '':
        return render_to_response('userreg.html',{'idnone':'uid is null',"regsave":True})

    User.objects.create_user(username = uid,password = pwd,email='template@xxu.com')

    regsave = True
    regok = True
    return render_to_response('userreg.html',locals())



def showbooklist(request):
    '''首页显示书籍列表'''

    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])  #每页长及起妈偏移地址（切片start）
    #sortfield = request.GET['sortfield']
    total = Books.objects.all().count()
    objvalues = Books.objects.all().order_by('-updatetime')[offset:limit + offset]
    rows = list(objvalues.values('id','name','booktypes','detial'))
    rlt = {'total':total,'rows':rows}

    if len(rows) == 0:
        return HttpResponse('0')
    else:
        return HttpResponse(json.dumps(rlt),content_type = 'application/json')

def showchildbooklist(request):
    '''得到实际书籍文件'''

    parentid = int(request.GET['parentid'])
    #print('bookid:',parentid,request.GET['limit'])
    #limit = int(request.GET['limit'])
    #offset = int(request.GET['offset'])  #每页长及起妈偏移地址（切片start）
    total = BookFiles.objects.all().count()
    objvalues = BookFiles.objects.filter(id = parentid).order_by('name') #[0:100]#offset:limit + offset]
    rows = list(objvalues.values('id','name'))
    rlt = {'total':total,'rows':rows}
    print(rlt)
    if len(rows) == 0:
        return HttpResponse('0')
    else:
        return HttpResponse(json.dumps(rlt),content_type = 'application/json')


def showsoftlist(request):
    '''首页显示软件列表'''

    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])  #每页长及起妈偏移地址（切片start）
    total = Softs.objects.all().count()
    objvalues = Softs.objects.all().order_by('-updatetime')[offset:limit + offset]
    rows = list(objvalues.values('id','name','softtypes','detial'))
    rlt = {'total':total,'rows':rows}

    if len(rows) == 0:
        return HttpResponse('0')
    else:
        return HttpResponse(json.dumps(rlt),content_type = 'application/json')

