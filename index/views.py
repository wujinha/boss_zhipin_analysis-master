from django.shortcuts import redirect, render
from django.http.response import JsonResponse
from django.http.request import HttpRequest
from django.http import HttpResponseRedirect
from django.urls.base import reverse
from auth.views import login_required
from urllib.parse import urlparse
# Create your views here.

# 渲染首页前端页面
@login_required
def index(request):
    return render(request, 'index.html')

# 渲染职位详情前端页面
@login_required
def detail(request, jobid):
    return render(request, 'detail.html', context=dict(jobid=jobid))

# 渲染登录注册前端页面
def login(request: HttpRequest):
    # 已登陆的状态，就直接进入主页
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    # 如果没登陆的话，就登陆
    return render(request, 'login.html')
