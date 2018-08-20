from django.db import models

# Create your models here.
"""
徐潇
2018-08-19
设计一个培训考试练习工具
"""


class Qts_userid(models.Model):
    '''考试ID，系统自动生成'''
    name = models.CharField(max_length = 20,default = '自动生成用户')
    id_date = models.DateTimeField(auto_now_add = True)
    id_ip = models.IPAddressField()  #生成日期、客户端ip地址
    id_password = models.CharField(max_length = 10,default = '111111')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Qts_Profession(models.Model):
    '''题库专业分类'''
    name = models.CharField(max_length = 50)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Qts_library(models.Model):
    '''题库'''
    '''备选答案choosableanswer字段：保存为一个长字符串。
        判断题直接为 T/F;
        单选与多选每个备选答案用 ||| 分隔开，每条备选第一个字符为 T/F分别代表该条是否为正确答案，当为多选时有多个正确答案;
        填空为所有答案的顺序列表，无空格用逗号分开;
        其它为最终答案'''
    qts_profession = models.ForeignKey(Qts_Profession,on_delete = models.CASCADE) #专业分类
    qts_types = models.CharField(max_length = 10)  #题型 判断、单选、多选、填空、简答、分析
    name = models.TextField() #题目内容
    choosableanswer = models.TextField() #备选答案
    trainnums = models.IntegerField(default = 0)
    examnums = models.IntegerField(default = 0) #访问（出题、练习次数）
    correctnums = models.IntegerField(default = 0)
    errornums = models.IntegerField(default = 0) #练习、考试正确错误次数
    qts_setter = models.CharField(max_length = 20,default = 'none') #出题人
    qts_source = models.CharField(max_length = 40,default = 'none') #题目来源
    qts_level = models.IntegerField(defautl = 0) #题目级别（难度,0 1 2 3）
    qts_date = models.DateTimeField(auto_now_add = True)  #上传日期


    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Qts_testpapers(models.Model):
    '''测试考试试卷列表'''
    userid = models.ForeignKey(Qts_userid)
    testpaperserial = models.CharField(max_length = 12) #试卷号 T\E开头分别代表练习、测试，T20180101120000000,标志 + 日期时间 + 子卷号
    testpaperdate = models.DateTimeField(auto_now_add = True) #试卷日期
    testpaperdetail = models.TextField()  #该张试卷详细 用json.dumps 生成字符串，可直接用 json.loads()生成对象
    """
    试卷详情：为一个字典
    {
       'qts_singlechoice' : [题号列表],  #单项选择题列表
       'qts_multichoice' : [题号列表],  #多项选择题列表
       'qts_judge' : [题号列表], #判断题列表
       'qts_gapfilling' :[....],  #填空题列表
       'qts_shortanswer' : [...], #简答
       'qts_analyze' : [...], #分析题
       'rltqts_error' : [[singlelist],[multilist],[judgelist],[shortanswerlist],[analyze]], #答错题列表,按序保存
       'rltqts_correct' : [[singlelist],[multilist],[judgelist],[shortanswerlist],[analyze]], #答对题列表,按序保存
       'score' : [float,],  #得分列表，跟上面一样的顺序
       'scoring_rate' : [得分率%,] #顺序同上
       'totalscore' : float,
       'totalscoring_rate' : str%,  #总得分、总得分率
    }
    """

