"""
2018-04-03
徐潇
"""

from django.db import models

class SoftType(models.Model):
    '''类别'''
    name = models.CharField(max_length = 20)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name'] 


class Softs(models.Model):
    '''软件信息'''
    name = models.CharField(max_length = 60)
    softtype = models.ForeignKey(SoftType,on_delete = models.CASCADE)  #2.0开始要加 on_delete
    detial = models.TextField(verbose_name = '内容简介')  
    accessnums = models.IntegerField(default = 0)
    updatetime = models.DateTimeField(auto_now_add = True,verbose_name = '上传时间')
    updateuser = models.CharField(max_length = 30,verbose_name = 'uploaduser',default = 'defaultuser')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class SoftFiles(models.Model):
    '''书籍的软件文件'''
    name = models.CharField(max_length = 60,verbose_name = '名称')  #文件名称
    soft_list = models.ForeignKey(Softs,on_delete = models.CASCADE) #指向 Books
    uploadfile = models.FileField(upload_to='software/%Y/%m/%d/',verbose_name = '文件') #文件路径 直接挂在 MEDIA_ROOT
    accessnums = models.IntegerField(verbose_name = '访问次数',default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

