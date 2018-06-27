from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import StreamingHttpResponse
from django.utils.http import urlquote
from datetime import datetime
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

#加密长字符串,传入是正常字符串,返回的是
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

    costtype = request.GET['costtype']
    costsubject = request.GET['costsubject']
    year = request.GET['year']
    month = request.GET['month']
    sqlstr = ''
    if costtype != 'all':
        sqlstr = 'costtype = {0}'.format(costtype)
    if costsubject != 'all':
        sqlstr = 'costsubject = {0}'.format(costsubject) if len(sqlstr) == 0 else '{0},costsubject = {1}'.format(sqlstr,costsubject)
    if year != 'all':
        sqlstr = 'year = {0}'.format(year) if len(sqlstr) == 0 else '{0},year = {1}'.format(sqlstr,year)
    if month != 'all':
        sqlstr = 'month = {0}'.format(month) if len(sqlstr) == 0 else '{0},month = {1}'.format(sqlstr,month)
    #生成查询过滤条件
    print(sqlstr)


    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])  #每页长及起妈偏移地址（切片start）
    
    total = Money.objects.all().count()
    #objvalues = Money.objects.all().order_by("-{0}".format(request.GET['sortfield'])).filter(sqlstr)
    objvalues = Money.objects.filter(year=2018)

    #[offset:limit + offset]

    rows = list(objvalues.values('date','costtype','costsubject','money','name'))  #[0:20])
    """取得数据，并生成一个列表，下面将日期转为字符串，外键转为名称
    """

    (prikey,pubkey) = getpubprikey(os.environ["HOME"] + "/.pri")

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
