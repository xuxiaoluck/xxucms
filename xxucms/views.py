from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib import auth
#from django.template.context_processors import csrf
from django.template import RequestContext
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from ebook.models import Books


def index(request):
    """主页,显示最新上传的五个软件、文章、图书"""

    bookn = Books.objects.order_by('updatetime')[:5]  #按更新时间取最新的五条图书数据
    bookrlt = [] #书籍列表
    for book in bookn:  #附件生成下拦菜单
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


    return render_to_response('index.html',locals())

def xlogin(request):
    '''登录视图'''

    uid = request.POST.get('uid','')
    pwd = request.POST.get('pwd','')
    user = auth.authenticate(username = uid,password = pwd)

    if user is not None and user.is_active:
        auth.login(request,user)

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



