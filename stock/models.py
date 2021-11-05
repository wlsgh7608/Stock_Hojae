from enum import unique
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import BigIntegerField, IntegerField
from django.contrib.auth import get_user, get_user_model


# Create your models here.
User = get_user_model()


class UsStocklist(models.Model):
    symbol = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=100)
    industry = models.CharField(max_length=50)
    industry_id = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'us_stocklist'



class UsCompanyDaily(models.Model):
    id = models.AutoField(primary_key=True,auto_created=True)
    stock_date = models.DateField()
    company_code = models.ForeignKey(UsStocklist,on_delete=CASCADE)
    close = models.FloatField(blank = True, null = True)
    open = models.FloatField(blank = True, null = True)
    high = models.FloatField(blank = True, null = True)
    low = models.FloatField(blank = True, null = True)
    volume = models.IntegerField(blank = True, null = True)
    change = models.FloatField(blank = True, null = True)
    class Meta:
        unique_together =(('company_code','stock_date'),)
        ordering = ['-stock_date']

class IncomeStatement(models.Model):
    id = models.AutoField(primary_key=True,auto_created=True)
    company_code = models.ForeignKey(UsStocklist,on_delete=CASCADE, null= False,default ='')
    end_date = models.DateField() # 날짜
    revenue = models.IntegerField(default=0,null=True) # 매출
    gross_profit = models.IntegerField(default =0,null=True) # 매출총이익 = 매출 - 매출원가
    operating_income = models.IntegerField(default= 0,null=True) # 영업이익 = 매출총이익 - (판매비+관리비)
    net_income = models.IntegerField(default = 0,null=True) # 당기순이익 = 세후 순이익
    
    class Meta:
        db_table = 'incomestatement'
        unique_together =(('company_code','end_date'),)
        ordering = ['-end_date']
       

class BalanceSheet(models.Model):
    id = models.AutoField(primary_key=True,auto_created=True)
    company_code = models.ForeignKey(UsStocklist,on_delete=CASCADE, null= False,default ='')
    end_date = models.DateField()# 날짜
    
    total_liability = BigIntegerField(default=0,null=True) # 총부채비용
    total_stockholder_equity = BigIntegerField(default=0,null=True) # 자기자본
    total_assets = BigIntegerField(default=0,null=True) # 총 자산
    total_current_assets = BigIntegerField(default=0,null=True) # 유동 자산 : 1년 안에 현금화가능한 자산
    total_current_liability = BigIntegerField(default=0,null=True) # 유동 부채 : 1년 안에 갚아야하는 자산

    class Meta:
        db_table = 'balancesheet'
        unique_together =(('company_code','end_date'),)
        ordering = ['-end_date']


class notapply(models.Model):
    id = models.AutoField(primary_key=True,auto_created=True)
    anb = models.IntegerField()
    pub_date = models.DateField()



class Company(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=40)
    last_update = models.DateField()

    def __str__(self):
        return self.company
