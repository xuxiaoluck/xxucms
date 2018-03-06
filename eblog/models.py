from django.db import models

# Create your models here.
### 2018-02-07


class BlogType(models.Model):
    '''分类'''
    name = models.CharField(max_length = 20)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']  #按书籍名称升序排列

class Blogs(models.Model):
    '''blog内容'''

    name = models.CharField(max_length = 100)
    blogtype = models.ForeignKey(BlogType,on_delete = models.CASCADE)  #2.0开始要加 on_delete
    authors = models.CharField(max_length = 20)
    detial = models.TextField(verbose_name = '内容简介')   #内容
    accessnums = models.IntegerField(default = 0)
    thumbupnums = models.IntegerField(verbose_name = '点赞',default=0)
    updatetime = models.DateTimeField(auto_now_add = True)


    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
