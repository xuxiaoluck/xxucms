from django.db import models

'''
2018-06-14
'''

class CostType(models.Model):
    '''费用类别'''
    name = models.CharField(max_length = 24)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class CostSubject(models.Model):
    '''科目（分类下）'''
    name = models.CharField(max_length = 64)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Money(models.Model):
    '''收支明细'''
    name = models.TextField(max_length = 1024)
    costtype = models.ForeignKey(CostType,on_delete = models.PROTECT)
    costsubject = models.ForeignKey(CostSubject,on_delete = models.PROTECT)
    money = models.FloatField()
    date = models.DateTimeField(auto_now = False,auto_now_add = True)
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['date']

