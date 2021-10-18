from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.

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
