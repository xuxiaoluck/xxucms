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


class stock_basics(models.Model):
    '''股票基本数据'''
    code = models.CharField(max_length = 6)
    name = models.CharField(max_length = 20)
    industry = models.CharField(max_length = 20)
    area = models.CharField(max_length = 20)
    pe = models.FloatField()
    outstanding = models.FloatField() #流通股本(万)
    totals = models.FloatField() #总股本(万)
    totalAssets = models.FloatField() #总资产(万)
    liquidAssets = models.FloatField() #流动资产
    fixedAssets = models.FloatField() #固定资产
    reserved = models.FloatField() #公积金
    reservedPerShare = models.FloatField() #每股公积金
    esp = models.FloatField() #每股收益
    bvps = models.FloatField() #每股净资
    pb = models.FloatField() #市净率
    timeToMarket = models.IntegerField() #上市日期
    undp = models.FloatField() #未分利润
    perundp = models.FloatField() #每股未分配
    rev = models.FloatField() #收入同比(%)
    profit = models.FloatField() #利润同比(%)
    gpr = models.FloatField() #毛利率(%)
    npr = models.FloatField() #净利润率(%)
    holders = models.IntegerField() #股东人数


class stock_reports(models.Model):
    '''业绩报告主表'''
    code = models.CharField(max_length = 6)
    name = models.CharField(max_length = 20)
    esp = models.FloatField()  #每股收益
    eps_yoy = models.FloatField() #每股收益同比(%)
    bvps = models.FloatField #每股净资产
    roe = models.FloatField() #净资产收益率(%)
    epcf = models.FloatField() #每股现金流量(元)
    net_profits = models.FloatField()  #净利润(万元)
    profits_yoy = models.FloatField()  #净利润同比(%)
    distrib = models.CharField(max_length = 100)  #,分配方案
    report_date = models.CharField(max_length = 6) #发布年季

class stock_profit(models.Model):
    '''盈利能力'''
    code = models.CharField(max_length = 6)
    name = models.CharField(max_length = 20)
    roe = models.FloatField() #净资产收益率(%)
    net_profit_ratio = models.FloatField() #净利率(%)
    gross_profit_rate = models.FloatField()  #毛利率(%)
    net_profits = models.FloatField() #净利润(万元)
    esp = models.FloatField()  #每股收益
    business_income = models.FloatField() #,营业收入(百万元)
    bips = models.FloatField() #每股主营业务收入(元)
    report_date = models.CharField(max_length = 6) #发布年季

class stock_operation(models.Model):
    '''运营能力'''
    code = models.CharField(max_length = 6)
    name = models.CharField(max_length = 20)
    arturnover = models.FloatField() #应收账款周转率(次)
    arturndays = models.FloatField() #应收账款周转天数(天)
    inventory_turnover = models.FloatField() #存货周转率(次)
    inventory_days = models.FloatField() #存货周转天数(天)
    currentasset_turnover = models.FloatField()  #流动资产周转率(次)
    currentasset_days = models.FloatField() #流动资产周转天数(天)
    report_date = models.CharField(max_length = 6) #发布年季

class stock_growth(models.Model):
    '''成长能力'''
    code = models.CharField(max_length = 6)
    name = models.CharField(max_length = 20)
    mbrg = models.FloatField() #主营业务收入增长率(%)
    nprg = models.FloatField() #净利润增长率(%)
    nav = models.FloatField() #净资产增长率
    targ = models.FloatField() #总资产增长率
    epsg = models.FloatField() #每股收益增长率
    seg = models.FloatField() #股东权益增长率
    report_date = models.CharField(max_length = 6) #发布年季

    
class stock_deptpaying(models.Model):
    '''债务能力'''
    code = models.CharField(max_length = 6)
    name = models.CharField(max_length = 20)
    currentratio = models.FloatField()  #流动比率
    quickratio = models.FloatField()  #速动比率
    cashratio = models.FloatField()  #现金比率
    icratio = models.FloatField()  #利息支付倍数
    sheqratio = models.FloatField()  #股东权益比率
    adratio = models.FloatField()  #股东权益增长率
    report_date = models.CharField(max_length = 6) #发布年季

class stock_cashflow(models.Model):
    '''现金流'''
    code = models.CharField(max_length = 6)
    name = models.CharField(max_length = 20)
    cf_sales = models.FloatField()  #,经营现金净流量对销售收入比率
    rateofreturn = models.FloatField()  #资产的经营现金流量回报率
    cf_nm = models.FloatField()   #经营现金净流量与净利润的比率
    cf_liabilities = models.FloatField()   #经营现金净流量对负债比率
    cashflowratio = models.FloatField()  #现金流量比率
    report_date = models.CharField(max_length = 6) #发布年季

