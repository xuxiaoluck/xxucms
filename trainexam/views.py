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

from trainexam.models import Qts_Profession,Qts_userid,Qts_library,Qts_testpapers

"""题库格式（excel表，第一行、第一列对应程序的中 0行0列）
1、从一列开始为正式有效数据。第一、二行为标签、标识、备注、字段名称之类的数据，正式题库从第三行开始。
2、第1列为题型名称（取前两个词，[单项、单选、单项选择、单选择题]等都是一样，[多项、多选],[问答、简答、名词、解释],[分析、案例],[判断],[填空]）
3、第2列题目内容
4、第3列为备选答案
5、第4列为正确答案
6、第5列为难度、级别
7、第6列为来源
8、第7列为出题人
9、在倒入判断、问答、分析、填空时备选答案与正确答案都直接到字段中，单选、多选时把答案直接组合到备选项的前面，以便于把备选答案打乱出题。
"""


def importqts_singlechoice(request):
    '''倒入单项选择题库'''

