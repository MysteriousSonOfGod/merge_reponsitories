# coding=utf-8

from . import views
from django.urls import path

# 这里的 urlpatterns 千万别拼错，不然出错
urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('add2/<int:a>/<int:b>/', views.add2, name='add2')

]
