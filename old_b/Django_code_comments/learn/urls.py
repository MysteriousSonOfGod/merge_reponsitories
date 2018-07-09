# coding=utf-8

from . import views
from django.urls import path


app_name = 'learn'
# 这里的 urlpatterns 千万别拼错，不然出错
urlpatterns = [
    path('', views.home, name='home'),
    # path('add/', views.add, name='add'),
    # 在这里 redirect 重定向
    path('add/<int:a>/<int:b>/', views.old_add2_redirect),
    path('add2/<int:a>/<int:b>/', views.add2, name='add2'),

]
