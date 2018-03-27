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


class Books(models.Model):
    '''书籍模型'''
    name = models.CharField(max_length = 60,verbose_name = '图书名称')
    booktype = models.ForeignKey(BookType,on_delete = models.CASCADE)  #2.0开始要加 on_delete
    publisher = models.ForeignKey(Publisher,on_delete = models.CASCADE)
    authors = models.CharField(max_length = 100,verbose_name = '作者列表')
    detial = models.TextField(verbose_name = '内容简介')   #书籍描述
    accessnums = models.IntegerField(default = 0)
    thumbupnums = models.IntegerField(verbose_name = '点赞',default=0)
    updatetime = models.DateTimeField(auto_now_add = True,verbose_name = '上传时间')
    updateuser = models.CharField(max_length = 30,verbose_name = 'uploaduser',default = 'defaultuser')


    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class BookFiles(models.Model):
    '''书籍的实际文件，单独用一个表，这样可以把同类文件放在一个标题里，特别是在做文档管理时基本上都是多个文件的。'''
    name = models.CharField(max_length = 60,verbose_name = '名称')  #文件名称
    book_list = models.ForeignKey(Books,on_delete = models.CASCADE) #指向 Books
    uploadfile = models.FileField(upload_to='ebooks/%Y/%m/%d/',verbose_name = '文件') #文件路径 直接挂在 MEDIA_ROOT
    accessnums = models.IntegerField(verbose_name = '访问次数',default=0)


    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

