# coding=utf-8
from django.urls import path
from . import views

"""
# 添加命名空间，防止多个app同时使用detail这个url，同时要去template文件里修改为指向相应命名空间的视图
app_name = 'polls'
urlpatterns = [
    # the 'name' value as called by the {% url %} template tag
    # 所以如果你想修改某个视图的url，不用管模板，在此处修改即可
    # ex: /polls/2/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/4/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/3/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
    # ex: /polls/
    path('', views.index, name='index'),
]
"""

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]