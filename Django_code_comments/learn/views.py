from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def start_page(request):
    return HttpResponse("Hello, welcome to visit my blog.")


def index(request):
    return HttpResponse("Hello, welcome to learn.")


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
    return HttpResponse(str(c))


def add2(request, a, b):
    """
    Django 允许我们用更优雅的方式
    但这需要在 urlpatterns 添加正则表达式为本函数传参
    参数错误就会404
    """
    c = int(a) + int(b)
    return HttpResponse(str(c))

