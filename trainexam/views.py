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

from trainexam.models import Qts_Profession,Qts_userid,Qts_library,Qts_testpapers

"""题库格式（excel表，第一行、第一列对应程序的中 0行0列）
1、从一列开始为正式有效数据。第一行为标签、标识、备注、字段名称之类的数据，正式题库从第二行开始。
2、第1列为题型名称（取前两个词，[单项、单选、单项选择、单选择题]等都是一样，[多项、多选],
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


"""
import xlrd
#只能读不能写
book = xlrd.open_workbook('stu.xls')#打开一个excel
#book._all_sheets_count  属性所有页数
sheet = book.sheet_by_index(0)#根据顺序获取sheet
sheet2 = book.sheet_by_name('case1_sheet')#根据sheet页名字获取sheet
print(sheet.cell(0,0).value)#指定行和列获取数据
print(sheet.cell(0,1).value)
print(sheet.cell(0,2).value)
print(sheet.cell(0,3).value)
print(sheet.ncols)#获取excel里面有多少列
print(sheet.nrows)#获取excel里面有多少行
print(sheet.get_rows())#
for i in sheet.get_rows():
    print(i)#获取每一行的数据
print(sheet.row_values(0))#获取第一行
for i in range(sheet.nrows):#0 1 2 3 4 5
    print(sheet.row_values(i))#获取第几行的数据

print(sheet.col_values(1))#取第一列的数据
for i in range(sheet.ncols):
    print(sheet.col_values(i))#获取第几列的数据


import tempfile

temp = tempfile.NamedTemporaryFile(suffix='_suffix', 
                                   prefix='prefix_', 
                                   dir='/tmp',
                                   )
try:
    print 'temp:', temp
    print 'temp.name:', temp.name
finally:
    temp.close()

"""


def import_qtsfiles(request):
    '''接收上传的文件，xls、xlsx'''
    """
    fobj = request.FILES.getlist('my-files')
    baseDir = os.path.dirname(os.path.abspath(__name__));
    jpgdir = os.path.join(baseDir,'static','jpg');
    filename = os.path.join(jpgdir,f.name);
    fobj = open(filename,'wb');
    for chrunk in f.chunks():
        fobj.write(chrunk);
    fobj.close();
    """



