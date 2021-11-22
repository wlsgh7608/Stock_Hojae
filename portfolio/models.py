from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.deletion import CASCADE
from django.db.models.expressions import OrderBy
from stock.models import UsStocklist


User = get_user_model()
# Create your models here.


class PortfolioName(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE)
    name = models.CharField(max_length=30)
    isshare = models.BooleanField(default = False)
    share_date = models.DateTimeField(null= True,blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-share_date']


class Portfolio(models.Model):
    portfolio = models.ForeignKey(PortfolioName,on_delete=CASCADE)
    symbol = models.CharField(max_length=20) # 현금, 부동산 등 주식리스트에 없을 수 있음 -> foreignkey 사용 X
    number = models.PositiveIntegerField()
    value = models.FloatField()


