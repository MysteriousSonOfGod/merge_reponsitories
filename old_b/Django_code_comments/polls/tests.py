from django.test import TestCase
import datetime
from django.utils import timezone
from django.urls import reverse
# Create your tests here.

from .models import Question

"""
1、对于每个模型和视图都建立单独的 TestClass
2、每个测试方法只测试一个功能
3、给每个测试方法起个能描述其功能的名字
"""


def create_question(question_text, days):
    """
    创建一个共用函数发表问题，question_text 是问题内容，days 是到现在的偏移量
    如果为正就是未来发布，为负就是在过去
    :param question_text: <str>
    :param days: <int>
    :return: <Question Object>
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        当问题是将来时 was_published_recently() 应该返回False
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        self.assertIs(future_question.was_published_recently(), False)
        """
        发生了什么呢？以下是自动化测试的运行过程：
        
        python manage.py testpolls将会寻找polls应用里的测试代码
        它找到了django.test.TestCase的一个子类
        它创建一个特殊的数据库供测试使用
        它在类中寻找测试方法——以test开头的方法。
        在test_was_published_recently_with_future_question方法中，它创建了一个pub_date值为30天后的Question实例。
        接着使用assertls()方法，发现was_published_recently()返回了True，而我们期望它返回False。
        测试系统通知我们哪些测试样例失败了，和造成测试失败的代码所在的行号。
        """

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)

        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)

        self.assertIs(recent_question.was_published_recently(), True)


class QuestionIndexViewTexts(TestCase):

    def test_no_questions(self):
        """
        如果没有问题存在，页面应该显示 "No polls are available." 的信息
        我刚才认为应该用单数 is，结果发现 index.html 中用的 are，怪不得测试不通过
        这是因为我们在index.html中定义了latest_question_list为空时显示此消息
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        # >>> response
        # < TemplateResponse status_code = 200, "text/html; charset=utf-8" >
        # self.assertContains(response, text) 检测 response.content 内容是否包含text内容

        self.assertQuerysetEqual(response.context['latest_question_list'], [])
        # >>> response.context['latest_question_list']
        # < QuerySet[ < Question: what's wrong?>, <Question: what's new? >] >

    def test_past_question(self):
        """
        过去发布的问题应该显示在index页面
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question.>'])

    def test_future_question(self):
        """
        数据库会在每次调用测试方法前被重置，所以之前方法创建的投票已经没了，所以主页中应该没有任何投票。
        未来发布的问题不应该出现在index页面
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        如果未来和过去的问题同时存在，只有过去的问题应该被展示
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question.>'])

    def test_two_past_question(self):
        """
        问题索引页面应该显示多个问题
        注意我一开始没有在意两次create_question的先后顺序，列表顺序应该是先2后1，怪不得测试不通过
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'], ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )


class QuestionDetailViewTests(TestCase):

    def test_future_question(self):
        """
        对于未来的问题详情页面应该是404 not found
        """
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        对于过去的问题详情页面应该是question_text内容
        """
        past_question = create_question(question_text="Past question.", days=-4)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

