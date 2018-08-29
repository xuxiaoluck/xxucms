"""
徐潇
2018-08-20
"""

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import StreamingHttpResponse
from django.utils.http import urlquote
from django.utils.encoding import escape_uri_path
from datetime import datetime
import json,os
import xlrd #excel 读取
import tempfile

from trainexam.models import Qts_Profession,Qts_Userid,Qts_Library,Qts_Testpapers

"""题库格式（excel表，第一行、第一列对应程序的中 0行0列）
1、从一列开始为正式有效数据。第一行为格式说明：第一列为 题库分类，第二列为 备选项的分隔符，第三列是为备选项是否有序号
   第二行为标签、标识、备注、字段名称之类的数据，正式题库从第三行开始。
2、第1列为题型名称（取前两个词，[单项、单选、单项选择、单项选择题]等都是一样，[多项、多选],
   [问答、简答、名词、解释],[分析、案例],[判断],[填空]）
3、第2列题目内容
4、第3列为备选答案
5、第4列为正确答案
6、第5列为难度、级别
7、第6列为来源
8、第7列为出题人
9、第8列为备注
10、在倒入判断、问答、分析、填空时备选答案与正确答案都直接到字段中，单选、多选时把答案直接组合到备选项的前面，
   以便于把备选答案打乱出题。
"""

XXUSPLITCHAR = '|##|'  #　题库中分隔备选答案的标记


def import_qtsjudge(onerowflag,onerowdata):
    '''倒入判断题,参数：标志行，只要前面一个;一行题目数据'''
    protype = onerowflag[0].strip()
    answey = 'F'
    """
    qts_profession 外键,专业分类 qts_types #题型 判断、单选、多选、填空、简答、分析    name　#题目内容
    choosableanswer #备选答案 trainnums examnums  #访问（出题、练习次数） correctnums errornums  #练习、考试正确错误次数
    qts_setter #出题人 qts_source #题目来源 qts_level #题目级别（难度,0 1 2 3） qts_date  #上传日期
    onerowdata 顺序：题型 题目内容 可选项 答案 难度	来源 出题人 memo

    """
    if onerowdata[3].strip().upper() in ['T','Ｔ','1','TRUE','OK','正确','对','ＯＫ','是','A','Ａ']:  #第４列（从０开始叫第３列）为答案
        answey = 'T'

    qtsdetail = onerowdata[1].strip() #第二列为内容
    tmpobj = Qts_Profession.objects.filter(name = protype)
    if tmpobj.count() == 0: #新的分类
        tmpobj = Qts_Profession(name = protype)
        tmpobj.save()

    addobj = Qts_Library(qts_types = '判断',name = qtsdetail,qts_profession = tmpobj,choosableanswer = answey, \
                          qts_level = onerowdata[4].strip(),qts_source = onerowdata[5].strip(),qts_setter = onerowdata[6].strip(), \
                          qts_memo = onerowdata[7].strip()) #其它字段默认
    addobj.save()

def import_qtssinglechoice(onerowflag,onerowdata):
    '''单选。参数：标志行，分别为专业分类、备选项分隔符、备选项是否带符号；题目内容'''

    protype = onerowflag[0].strip()
    splitchar = onerowflag[1].strip()
    isexistserial = onerowflag[2].strip()

    answey = onerowdata[3].strip().upper() #答案
    qtsdetail = onerowdata[1].strip() #第二列为内容
    tmpobj = Qts_Profession.objects.filter(name = protype)
    if tmpobj.count() == 0: #新的分类
        tmpobj = Qts_Profession(name = protype)
        tmpobj.save()

    choosableansweystr = onerowdata[2].strip() #对可选答案进行分析，把正确答案标志放到　选项前面第一个字符
    answeylist = choosableansweystr.split(splitchar) #分隔选项 ord('A') - 1 = 64,ord('中文A') - 1 = 65312
    answeylist[ord(answey) - 65] = 'T...' + answeylist[ord(answey) - 65]
    #正确答案做标记， ABCDEFG等前与0刚好相关６５
    addobj = Qts_Library(qts_types = '单选题',name = qtsdetail,qts_profession = tmpobj,choosableanswer = XXUSPLITCHAR.join(answeylist), \
                          qts_level = onerowdata[4].strip(),qts_source = onerowdata[5].strip(),qts_setter = onerowdata[6].strip(), \
                          qts_memo = onerowdata[7].strip())
    addobj.save()

def import_qtsmultichoice(onerowflag,onerowdata):
    '''多选。参数：标志行，分别为专业分类、备选项分隔符、备选项是否带符号；题目内容'''

    protype = onerowflag[0].strip()
    splitchar = onerowflag[1].strip()
    isexistserial = onerowflag[2].strip()

    trueanswey = onerowdata[3].strip().upper() #答案列表
    qtsdetail = onerowdata[1].strip() #第二列为内容
    tmpobj = Qts_Profession.objects.filter(name = protype)
    if tmpobj.count() == 0: #新的分类
        tmpobj = Qts_Profession(name = protype)
        tmpobj.save()

    choosableansweystr = onerowdata[2].strip() #对可选答案进行分析，把正确答案标志放到　选项前面第一个字符
    answeylist = choosableansweystr.split(splitchar) #分隔选项　　1 A 64,1 Ａ　65312


    for item in trueanswey:
        answeylist[ord(item) - 65] = 'T...' + answeylist[ord(item) - 65]
    #正确答案做标记， ABCDEFG等前与0刚好相关６５,多选有多个答案
    addobj = Qts_Library(qts_types = '多选题',name = qtsdetail,qts_profession = tmpobj,choosableanswer = XXUSPLITCHAR.join(answeylist), \
                          qts_level = onerowdata[4].strip(),qts_source = onerowdata[5].strip(),qts_setter = onerowdata[6].strip(), \
                          qts_memo = onerowdata[7].strip())
    addobj.save()


def import_qtsgapfilling(onerowflag,onerowdata):
    '''填空。参数：标志行，；题目内容'''

    protype = onerowflag[0].strip()
    answey = onerowdata[3].strip().upper() #
    qtsdetail = onerowdata[1].strip() #第二列为内容
    tmpobj = Qts_Profession.objects.filter(name = protype)
    if tmpobj.count() == 0: #新的分类
        tmpobj = Qts_Profession(name = protype)
        tmpobj.save()

    addobj = Qts_Library(qts_types = '填空题',name = qtsdetail,qts_profession = tmpobj,choosableanswer = answey,\
                          qts_level = onerowdata[4].strip(),qts_source = onerowdata[5].strip(),qts_setter = onerowdata[6].strip(), \
                          qts_memo = onerowdata[7].strip())
    addobj.save()

def import_qtsanalyze(onerowflag,onerowdata):
    '''分析。参数：标志行，；题目内容'''

    protype = onerowflag[0].strip()
    answey = onerowdata[3].strip().upper() #
    qtsdetail = onerowdata[1].strip() #第二列为内容
    tmpobj = Qts_Profession.objects.filter(name = protype)
    if tmpobj.count() == 0: #新的分类
        tmpobj = Qts_Profession(name = protype)
        tmpobj.save()

    addobj = Qts_Library(qts_types = '分析题',name = qtsdetail,qts_profession = tmpobj,choosableanswer = answey,\
                          qts_level = onerowdata[4].strip(),qts_source = onerowdata[5].strip(),qts_setter = onerowdata[6].strip(), \
                          qts_memo = onerowdata[7].strip())
    addobj.save()

def import_qtsshortanswey(onerowflag,onerowdata):
    '''简答。参数：标志行，；题目内容'''

    protype = onerowflag[0].strip()
    answey = onerowdata[3].strip().upper() #
    qtsdetail = onerowdata[1].strip() #第二列为内容
    tmpobj = Qts_Profession.objects.filter(name = protype)
    if tmpobj.count() == 0: #新的分类
        tmpobj = Qts_Profession(name = protype)
        tmpobj.save()

    addobj = Qts_Library(qts_types = '简答题',name = qtsdetail,qts_profession = tmpobj,choosableanswer = answey,\
                          qts_level = onerowdata[4].strip(),qts_source = onerowdata[5].strip(),qts_setter = onerowdata[6].strip(), \
                          qts_memo = onerowdata[7].strip())
    addobj.save()







"""以下为与 template 交互"""



def index(request):
    '''打开首页'''

    return render_to_response('trainexam.html',locals())

def autogenuser00001(request):
    '''自动生成用户'''

    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']

    userobj = Qts_Userid(name = 'autogenuser',id_ip = ip)
    userobj.save()
    return HttpResponse('登录ID：{0}\n用户名:{1}\n请使用ID登录系统\n用户名可自行更改'.format(userobj.id,userobj.name))

def userlogin00001(request):
    '''登录考试系统'''
    

def import_qtsfiles(request):
    '''接收上传的文件，xls、xlsx'''

    fobjs = request.FILES.getlist('my-files')  #得到上传的所有文件对象
    for onefile in fobjs:
        suffix = os.path.splitext(onefile.name)[1]  #得到扩展名，作为临时文件后缀
        tempfileobj = tempfile.NamedTemporaryFile(suffix=suffix,prefix='xxu')  #生成一个临时文件
        ftempobj = open(tempfileobj.name,'wb')
        for chrunk in onefile.chunks():  #写入临时文件
            ftempobj.write(chrunk)
        ftempobj.close()  #生成数据
        book = xlrd.open_workbook(tempfileobj.name)  #打开 xlsx文件
        sheetcount = book._all_sheets_count #总页数
        for i in range(sheetcount):
            onesheet = book.sheet_by_index(i)  #取一页
            nrows = onesheet.nrows  #行数
            onerowflag = onesheet.row_values(0)  #得标志行数据
            for j in range(2,nrows):  #从第三行开始为正式的题库数据
                onerowdata = onesheet.row_values(j)
                if onerowdata[0].strip() in ['判断','判断题']:
                    import_qtsjudge(onerowflag,onerowdata)  #倒入判断题
                elif onerowdata[0].strip() in ['单选','单项','单项选择','单项选择题','单选题']:
                    import_qtssinglechoice(onerowflag,onerowdata)
                elif onerowdata[0].strip() in ['多选','多项','多项选择','多项选择题','多选题']:
                    import_qtsmultichoice(onerowflag,onerowdata)
                elif onerowdata[0].strip() in ['填空','填空题','完形填空']:
                    import_qtsgapfilling(onerowflag,onerowdata)
                elif onerowdata[0].strip() in ['简答','解释','名词解释','问答','问答题','简答题','解释题']:
                    import_qtsshortanswey(onerowflag,onerowdata)
                elif onerowdata[0].strip() in ['分析','案例题','案例分析','案例','分析题','案例分析题']:
                    import_qtsanalyze(onerowflag,onerowdata)

        tempfileobj.close()
