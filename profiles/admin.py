from django.contrib import admin

from profiles.models import BookMark, TodoList

# Register your models here.



admin.site.register(TodoList)
admin.site.register(BookMark)
