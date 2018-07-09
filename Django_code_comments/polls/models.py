import datetime

from django.db import models
from django.utils import timezone

# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        # return self.pub_data >= timezone.now() - datetime.timedelta(days=1)
        # 经过测试并已修正
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    # 这里通过附加函数属性使得这个方法获得了在管理后台的排序，显示规则
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
