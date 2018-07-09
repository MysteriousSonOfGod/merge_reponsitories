from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
# Create your views here.


def home(request):
    tutorial_list = ["HTML", "CSS", "jQuery", "Python", "Django"]
    info_dict = {'site': '付东来', 'content': '瞎BB'}
    generator = map(str, range(100))
    return render(request, template_name='learn/home.html',
                  context={
                      'tutorial_list': tutorial_list,
                      'info_dict': info_dict,
                      'generator': generator,
                      'request': request,

                  })


def index(request):
    return render(request, 'learn/home.html')


def add(request):
    """
    采用 /add/?a=4&b=5 这样GET方法进行访问
    request.GET 类似于一个字典，更好的办法是用 request.GET.get('a', 0) 当没有传递 a 的时候默认 a 为 0

    """
    # a = request.GET['a']
    a = request.GET.get('a', 1)
    # b = request.GET['b']
    b = request.GET.get('b', 2)
    c = int(a) + int(b)
    return HttpResponse('add = ' + str(c))


def add2(request, a, b):
    """
    Django 允许我们用更优雅的方式
    但这需要在 urlpatterns 添加正则表达式为本函数传参
    参数错误就会404
    """
    c = int(a) + int(b)
    # print(reverse('learn:add2', args=(a, b,)))
    return HttpResponse('add2 = ' + str(c))


def old_add2_redirect(request, a, b):
    # a = request.GET.get('a', 1)
    # b = request.GET.get('b', 2)
    # 这里 redirect 到了 add2 网址
    return HttpResponseRedirect(reverse('learn:add2', args=(a, b)))

