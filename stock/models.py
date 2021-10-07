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

class Company(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=40)
    last_update = models.DateField()

    def __str__(self):
        return self.company


class Daily(models.Model):
    company_code = models.ForeignKey(UsStocklist,on_delete=CASCADE)
    company_name = models.CharField(max_length=40)
    date = models.DateField()
    open = models.IntegerField()
    high = models.IntegerField()
    low = models.IntegerField()
    close = models.IntegerField()
    volume = models.IntegerField()

    def __str__(self):
        return self.company_name