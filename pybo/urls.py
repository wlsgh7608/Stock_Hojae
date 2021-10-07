from django.urls import path,include


from . import views

app_name = 'pybo'

urlpatterns = [
    path('',views.index, name = 'index'),
    path('<int:question_id>/',views.detail, name = 'detail'),
  
]