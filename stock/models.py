from django.db import models

# Create your models here.
"""
2018-04-12 徐潇
"""


class stock_industry(models.Model):
    '''行业分类:代码、名称、行业名称'''
    code = models.CharField(max_length = 6)
    name = models.CharField(max_length = 20)
    i_name = models.CharField(max_length = 20)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['code']


class stock_concept(models.Model):
    '''概念分类:代码、名称、概念名称'''
    code = models.CharField(max_length = 6)
    name = models.CharField(max_length = 20)
    c_name = models.CharField(max_length = 20)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['code']


class stock_area(models.Model):
    '''地域分类:代码、名称、地域'''
    code = models.CharField(max_length = 6)
    name = models.CharField(max_length = 20)
    a_name = models.CharField(max_length = 20)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['code']

class stock_sme(models.Model):
    '''中小板:代码、名称'''
    code = models.CharField(max_length = 6)
    name = models.CharField(max_length = 20)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['code']

class stock_gem(models.Model):
    '''创业板:代码、名称'''
    code = models.CharField(max_length = 6)
    name = models.CharField(max_length = 20)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['code']


class stock_st(models.Model):
    '''ST板:代码、名称'''
    code = models.CharField(max_length = 6)
    name = models.CharField(max_length = 20)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['code']

class stock_hs300(models.Model):
    '''沪深300:代码、名称、日期、权重'''
    code = models.CharField(max_length = 6)
    name = models.CharField(max_length = 20)
    date = models.DateField()
    weight = models.CharField(max_length = 5)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['code']


class stock_sz50(models.Model):
    '''上证300:代码、名称'''
    code = models.CharField(max_length = 6)
    name = models.CharField(max_length = 20)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['code']

class stock_zz500(models.Model):
    '''zz500:代码、名称'''
    code = models.CharField(max_length = 6)
    name = models.CharField(max_length = 20)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['code']

class stock_terminate(models.Model):
    '''终止上市:代码、名称、上市日期、终止日期'''
    code = models.CharField(max_length = 6)
    name = models.CharField(max_length = 20)
    s_date = models.CharField(max_length = 10)
    e_date = models.CharField(max_length = 10)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['code']


class stock_suspend(models.Model):
    '''暂停上市:代码、名称、上市日期、暂停日期'''
    code = models.CharField(max_length = 6)
    name = models.CharField(max_length = 20)
    s_date = models.CharField(max_length = 10)
    e_date = models.CharField(max_length = 10)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['code']


