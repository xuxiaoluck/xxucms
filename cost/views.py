from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import StreamingHttpResponse
from django.utils.http import urlquote
from datetime import datetime
from django.conf import settings
import json,os
import rsa,binascii

from cost.models import CostType,CostSubject,Money


'''2018-06-14
'''

#解密用
def getpubprikey(keypath):
        prifile = open(keypath + '/rsapri.pem')
        pdata = prifile.read()
        prikey = rsa.PrivateKey.load_pkcs1(pdata)
        prifile.close()

        pubfile = open(keypath + '/rsapub.pem')
        pdata = pubfile.read()
        pubkey = rsa.PublicKey.load_pkcs1(pdata)
        pubfile.close()
        return (prikey,pubkey)

#加密长字符串,传入是正常字符串,返回的是 HEX加密字符串列表，保存时转为以逗号为隔的字符
def encryptlongstr(longstr,pubkey):
        encodestr = longstr.encode()
        strlen = len(encodestr)
        onestrlen = 1024 // 8 - 11  #每小段长
        (seconds,modlen) = (strlen // onestrlen,strlen % onestrlen)  #得到总共段数及余下长度
        minwenlist = []
        enwenlist = []
        for i in range(seconds):
            minwen = encodestr[i * onestrlen: i * onestrlen + 117] #得到一段明文
            enwen = rsa.encrypt(minwen,pubkey)
            minwenlist.append(minwen)
            enwenlist.append(binascii.hexlify(enwen).decode())
        if modlen > 0: #有余下部分
            minwen = encodestr[0 - modlen:]
            enwen = rsa.encrypt(minwen,pubkey)
            minwenlist.append(minwen)
            enwenlist.append(binascii.hexlify(enwen).decode())

        #当有中文等非1-128字符时，encrypt加密后的结果在解密后不能正常用decode得到原文，可对原加密数据用 hexlify包装成16进制字符串
        return enwenlist


def decryptlongstr(longstrlist,prikey):
        """解密， 列表中的每一项都是用 hexlify包装过的16进制字符串，每项正常用unhexify反包装后进行解密，得到 encode串，
        由于有中文存在，可能在项中存在半个中文的情况，要全部连接后才能decode()后得到正确的字符串。返回解密后的串。
        """

        if len(longstrlist) == 0:
            return []

        minwenlist = []
        for item in longstrlist:
            if len(item)== 0:
                continue
            minwen = rsa.decrypt(binascii.unhexlify(item),prikey)
            #print(minwen)
            minwenlist.append(minwen)
        #对hexlify字符串进行unhexlify再解密，主要针对非1-127字符
        minwenstr = b''
        for item in minwenlist:
            minwenstr += item

        return minwenstr.decode()


def index(request):
    '''首页'''

    #先验证是否登录
    if not request.user.is_authenticated:
        return render_to_response('nologin.html',locals())

    typelist = list(CostType.objects.all().values())  #得到所有类型列表，每条为一个字典,KEY为字段名
    subjectlist = list(CostSubject.objects.all().values().order_by('name'))
    yearlist = Money.objects.values('year').order_by('-year').distinct()
    monthlist = range(1,13)
    return render_to_response('cost.html',locals())

def getcostinfo(request):
    '''显示数据'''


    if not request.user.is_authenticated:
        return render_to_response('nologin.html',locals())

    costtype = request.GET['costtype']
    costsubject = request.GET['costsubject']
    year = request.GET['year']
    month = request.GET['month']
    sqldict = {}
    if costtype != 'all':
        sqldict['costtype'] = costtype
    if costsubject != 'all':
        sqldict['costsubject'] = costsubject
    if year != 'all':
        sqldict['year'] = year
    if month != 'all':
        sqldict['month'] = month
    #生成查询过滤条件

    sortfield = request.GET['sortfield']

    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])  #每页长及起妈偏移地址（切片start）

    if len(sqldict) == 0:
        total = Money.objects.all().count()
    else:
        total = Money.objects.filter(**sqldict).count()

    if len(sqldict) == 0:
        if sortfield == 'date':
            objvalues = Money.objects.all().order_by('-date','costtype','costsubject')[offset:limit + offset]
        elif sortfield == 'costtype':
            objvalues = Money.objects.all().order_by('costtype','-date','costsubject')[offset:limit + offset]
        elif sortfield == 'costsubject':
            objvalues = Money.objects.all().order_by('costsubject','-date','costtype')[offset:limit + offset]
        else:
            objvalues = Money.objects.all().order_by('-money','costtype','costsubject')[offset:limit + offset]
    else:
        if sortfield == 'date':
            objvalues = Money.objects.filter(**sqldict).order_by('-date','costtype','costsubject')[offset:limit + offset]
        elif sortfield == 'costtype':
            objvalues = Money.objects.filter(**sqldict).order_by('costtype','-date','costsubject')[offset:limit + offset]
        elif sortfield == 'costsubject':
            objvalues = Money.objects.filter(**sqldict).order_by('costsubject','-date','costtype')[offset:limit + offset]
        else:
            objvalues = Money.objects.filter(**sqldict).order_by('-money','costtype','costsubject')[offset:limit + offset]

    #[offset:limit + offset]

    rows = list(objvalues.values('date','costtype','costsubject','money','name'))  #[0:20])
    """取得数据，并生成一个列表，下面将日期转为字符串，外键转为名称
    """

    if settings.ISSERVER == 'NO':
        (prikey,pubkey) = getpubprikey("/home/xuxiaoc/.pri")
    elif settings.ISSERVER == 'YES':
        (prikey,pubkey) = getpubprikey("/home/xuxiaos/.pri")
    else:
        (prikey,pubkey) = getpubprikey("/home/xuxiao/.pri")

    for item in rows:
        tmpstr = item['date'].strftime("%Y-%m-%d")
        item['date'] = tmpstr
        tmpid = item['costtype']
        tmpname = CostType.objects.get(id = tmpid).name
        item['costtype'] = tmpname

        tmpid = item['costsubject']
        tmpname = CostSubject.objects.get(id = tmpid).name
        item['costsubject'] = tmpname

        tmpstr = decryptlongstr(item['name'].split(','),prikey)
        item['name'] = tmpstr  #名称解密，原始文件经过加密处理



    rlt = {'total':total,'rows':rows}

    #print('total','limit:{0},offset:{1}'.format(limit,offset),total)

    if len(rows) == 0:
        return HttpResponse('0')
    else:
        return HttpResponse(json.dumps(rlt),content_type = 'application/json')


def openinputcost(request):
    """打开录入收支数据"""
    if not request.user.is_authenticated:
        return render_to_response('nologin.html',locals())

    typelist = list(CostType.objects.all().values())  #得到所有类型列表，每条为一个字典,KEY为字段名
    subjectlist = list(CostSubject.objects.all().values().order_by('name'))

    return render_to_response('inputcost.html',locals())


"""
保存数据时的备注数据为加密保存
encryptlongstr:传入的一个长字符串、公钥，返回的是一个 hex16进制形式的字符串列表（所以长度至少是原长的2倍）;
decryptlongstr:传入的是一个HEX16进制形式的字符串列表、私钥，返回解密后的长字符串;
保存时要把加密得到的密文列表用 ','.join(mistr)转成以逗号分隔的字符串，取出数据时直接解密。
"""
def addonecost(request):
        """增加一条收支数据"""

        if not request.user.is_authenticated:
                return render_to_response('nologin.html',locals())

        costdate = datetime.strptime(request.POST['costdate'],'%Y-%m-%d')
        costtypeid = request.POST['costtypeid']
        costsubjectid = request.POST['costsubjectid']
        costmoney = request.POST['costmoney']

        typeobj = CostType.objects.get(id = costtypeid)
        subjectobj = CostSubject.objects.get(id = costsubjectid)  #得到外键
        minstr = request.POST['costmemo']
        if settings.ISSERVER == 'NO':
            (prikey,pubkey) = getpubprikey("/home/xuxiaoc/.pri")
        elif settings.ISSERVER == 'YES':
            (prikey,pubkey) = getpubprikey("/home/xuxiaos/.pri")
        else:
            (prikey,pubkey) = getpubprikey("/home/xuxiao/.pri")

        milist = encryptlongstr(minstr,pubkey)
        #得到是以hex形式的字符串列表


        obj = Money(costtype = typeobj,costsubject = subjectobj,
                    date = costdate,year = costdate.year,month = costdate.month,day = costdate.day,
                    money = float(costmoney),name = ",".join(milist)
        )
        obj.save()

        return HttpResponse('<font color=red >(succ,ID:{0})</font>'.format(obj.id))


def addonetype(request):
        """增加一条分类数据"""
        typename = request.POST["typename"]

        rlt = {}
        rlt['exists'] = False
        if CostType.objects.filter(name = typename).exists(): #True表示已存在
                rlt['exists'] = True
                rlt['info'] = '<font color=red>(分类已存在！)</font>'
        else:
                obj = CostType(name = typename)
                obj.save()
                rlt['exists'] = False
                rlt['info'] = '<font color=red>(succ,id={}！)</font>'.format(obj.id)
                rlt['id'] = obj.id

        return HttpResponse(json.dumps(rlt),content_type = 'application/json')


def addonesubject(request):
        """增加一条科目数据"""
        typename = request.POST["subjectname"]

        rlt = {}
        rlt['exists'] = False
        if CostSubject.objects.filter(name = typename).exists(): #True表示已存在
                rlt['exists'] = True
                rlt['info'] = '<font color=red>(科目已存在！)</font>'
        else:
                obj = CostSubject(name = typename)
                obj.save()
                rlt['exists'] = False
                rlt['info'] = '<font color=red>(succ,id={}！)</font>'.format(obj.id)
                rlt['id'] = obj.id

        return HttpResponse(json.dumps(rlt),content_type = 'application/json')

def opentotalcost(request):
        """打开统计总体数据、汇总明细"""

        if not request.user.is_authenticated:
                return render_to_response('nologin.html',locals())


        typelist = list(CostType.objects.all().values())  #得到所有类型列表，每条为一个字典,KEY为字段名
        subjectlist = list(CostSubject.objects.all().values().order_by('name'))

        return render_to_response('total.html',locals())

def totalcost(request):
        """统计总体数据、汇总明细"""

        rlt = ''
        return HttpResponse(json.dumps(rlt),content_type = 'application/json')