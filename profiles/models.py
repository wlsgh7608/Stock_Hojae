

from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.deletion import CASCADE




User = get_user_model()


class TodoList(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE)
    todolist = models.TextField()