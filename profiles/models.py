

from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.deletion import CASCADE
from stock.models import UsStocklist



User = get_user_model()


class TodoList(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE)
    todolist = models.TextField()


class BookMark(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    bookmark_symbol = models.ForeignKey(UsStocklist,on_delete= models.CASCADE)
    bookmark_date= models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-bookmark_date']


 
    