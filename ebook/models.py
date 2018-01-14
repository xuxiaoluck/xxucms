from django.db import models

"""电子图书模型"""

class BookType(models.Model):
    '''书籍模型'''
    name = models.CharField(max_length = 20,verbose_name = '分类名称')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']  #按书籍名称升序排列

class Publisher(models.Model):
    '''出版社'''
    name = models.CharField(max_length = 80,verbose_name = '出版社名称')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Author(models.Model):
    '''作者'''
    name = models.CharField(max_length = 50,verbose_name = '作者')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Books(models.Model):
    '''书籍模型'''
    name = models.CharField(max_length = 60,verbose_name = '图书名称')
    booktype = models.ForeignKey(BookType,on_delete = models.CASCADE)  #2.0开始要加 on_delete
    uploadfile = models.FileField(verbose_name = '文件',blank = True)
    publisher = models.ForeignKey(Publisher,on_delete = models.CASCADE)
    authors = models.ManyToManyField('Author')
    detial = models.TextField(verbose_name = '内容简介')   #书籍描述
    uploadtime = models.DateTimeField(auto_now_add = True,verbose_name = '上传时间')
    uploaduser = models.CharField(max_length = 30,verbose_name = '上传用户')
    accessnums = models.IntegerField(verbose_name = '访问次数')
    thumbupnums = models.IntegerField(verbose_name = '点赞')
    

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
