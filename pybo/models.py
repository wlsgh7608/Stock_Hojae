from django.contrib.auth import get_user_model
from django.db import models
from stock.models import UsStocklist
# Create your models here.

User = get_user_model()
class Blog(models.Model):
    symbol = models.ForeignKey(UsStocklist,on_delete= models.CASCADE,null= False,default ='')
    title = models.CharField(max_length=50)
    body = models.TextField()
    user = models.ForeignKey(User,related_name ='blogs', on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date= models.DateTimeField(null = True, blank = True)
    hits = models.IntegerField(default = 0)

    def __str__(self):
        return self.title


class Comment(models.Model):
    question = models.ForeignKey(Blog,on_delete=models.CASCADE,default= '')
    content = models.TextField()
    user = models.ForeignKey(User,related_name ='comments', on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date= models.DateTimeField(null = True, blank = True)

    def __str__(self):
        return self.content
