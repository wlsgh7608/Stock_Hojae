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

# class UsCompanyDay(models.Model):
#     id = models.AutoField(primary_key=True,auto_created=True)
#     stock_date = models.DateField()
#     company_code = models.ForeignKey(UsStocklist,on_delete=CASCADE)
#     close = models.FloatField(blank = True, null = True)
#     open = models.FloatField(blank = True, null = True)
#     high = models.FloatField(blank = True, null = True)
#     low = models.FloatField(blank = True, null = True)
#     volume = models.IntegerField(blank = True, null = True)
#     change = models.FloatField(blank = True, null = True)
#     class Meta:
#         unique_together =(('company_code','stock_date'),)
#         ordering = ['-stock_date']

class newDay(models.Model):
    abc = models.CharField(max_length=50)
class Company(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=40)
    last_update = models.DateField()

    def __str__(self):
        return self.company
