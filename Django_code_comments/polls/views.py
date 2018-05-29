from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone
# Create your views here.
from .models import Question, Choice

"""
def index(request):
    latest_question_list = Question.objects.order_by('-pub_data')[:5]
    # template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    # return HttpResponse(template.render(context, request))

    # render()是一个快捷函数，载入模板，填充上下文，再返回生成的 HTTPResponse 对象
    return render(request, 'polls/index.html', context)
"""


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    # 类似地，ListView 默认使用一个叫做 < appname > / < modelname > _list.html的默认模板；
    context_object_name = 'latest_question_list'
    # Django能够为context变量决定一个合适的名字。然而对于ListView， 自动生成的context变量是question_list
    # 为了覆盖这个行为，我们提供context_object_name属性，表示我们想使用latest_question_list。

    def get_queryset(self):
        """
        返回最后发布的5个问题。
        """
        # return Question.objects.order_by('-pub_date')[:5]
        #  这里order_by要用 '-' 接属性名，刚才写错了，老是出错
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
        # Question.objects.filter(pub_date__lte=timezone.now())
        # pub_date已经在modesls.py中申明过是Timefield类型，它的属性用双下划线访问
        # lte --> less than equal 选出比当前时间小的queryset


"""
def detail(request, question_id):
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404('Question does not exist')

    # get_object_or_404()是 Http404 错误的快捷函数
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
"""


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    # 默认情况下，通用视图DetailView使用一个叫做 < appname > / < modelname > _detail.html的模板。
    # 在我们的例子中，它将使用"polls/question_detail.html"模板。
    # template_name属性是用来告诉Django使用一个指定的模板名字，而不是自动生成的默认名字。

    def get_queryset(self):
        """
        排除还未发布的问题，以免用户猜出url访问到它们
        :return: <Queryset>
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


"""
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
"""


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # selected_choice = question.choice_set.get(pk=request.POST['choice'])
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        # request.POST 是一个类字典对象，让你可以通过关键字的名字获取提交的数据，获得的永远是字符串。
        # 我们在代码中显式地使用request.POST ，以保证数据只能通过POST调用改动。

    except (KeyError, Choice.DoesNotExist):
        # 若出错就重新显示 Question 表单。KeyError是可能POST表单无该键
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice."
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))  # '/polls/3/results/'
    # 你应该总是返回一个HttpResponseRedirect在一次POST数据之后，这不是Django特定，而是通用技巧
    # reverse()函数避免了我们在视图函数中硬编码URL。它需要我们给出我们想要跳转的视图的名字和该视图所对应的URL模式中需要给该视图提供的参数。


