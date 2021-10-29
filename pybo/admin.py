from django.contrib import admin
from .models import Blog, Comment
# Register your models here.

class BlogAdmin(admin.ModelAdmin):
    search_fields= ['title']

admin.site.register(Blog)
admin.site.register(Comment)


