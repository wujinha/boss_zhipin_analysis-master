import simplejson
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http.request import HttpRequest
from index.utils import success, error, redirect
from functools import wraps
from .models import Profile
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse

# 用户登录装饰器，用于限制必须登录的情况，如果没登录，重定向至登录页
def login_required(func):
    @wraps(func)
    def wrap(request: HttpRequest, *args, **kwargs):
        # 如果用户已登陆，允许访问
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        # 否则重定向回登陆页
        return HttpResponseRedirect(reverse('login'))
    return wrap

# 用户登录视图
def login_view(request: HttpRequest):
    # 如果用户已登陆，无需继续登陆
    if request.user.is_authenticated:
        return error('请勿重复登录')
    else:
        data = simplejson.loads(request.body)
        user = authenticate(request,
                            username=data.get('username'),
                            password=data.get('password'))
        if user:
            login(request, user)
            # 账号密码成功，进入主页面
            return redirect(reverse('home'))
        return error('帐号或密码错误')

# 用户注册视图
def signup(request):
    data = simplejson.loads(request.body)
    if not all((data.get('username'), data.get('password'), data.get('password2'))):
        return error('信息不全')
    if data.get('password') != data.get('password2'):
        return error('二次密码不一致')
    if User.objects.filter(username=data.get('username')).exists():
        return error('帐号已存在')
    user = User.objects.create_user(username=data.get('username'),
                                    password=data.get('password'),
                                    is_staff=True) #, is_superuser=True
    # 注册新用户
    user.save()
    login(request, user)
    # 进入主页面
    return redirect(reverse('home'))

# 用户注销视图
@login_required
def logout_view(request: HttpRequest):
    logout(request)
    # 注销以后返回登陆页面
    return HttpResponseRedirect(reverse('login'))

# 工具函数
def to_dict(l):
    def _todict(obj):
        j = {k: v for k, v in obj.__dict__.items() if not k.startswith('_')}
        return j
    return [_todict(i) for i in l]

# 获取用户信息视图
def get_profile(request):
    # 必须要登陆才能访问
    if not request.user.is_authenticated:
        return error('...')
    # 找到用户信息
    profile = Profile.objects.filter(userid=request.user.id)
    if profile:
        return JsonResponse(to_dict([profile[0]])[0])
    return JsonResponse({})

# 保存用户信息视图
def save_profile(request):
    if not request.user.is_authenticated:
        return error('...')
    try:
        data = simplejson.loads(request.body)
    except:
        data = {}
    data['userid'] = request.user.id
    # 找到用户信息
    profile = Profile.objects.filter(userid=request.user.id)
    # 已存在的话需要更新
    if profile:
        profile = profile[0]
        for k, v in data.items():
            setattr(profile, k, v)
        profile.save()
    # 不存在的话需要创建
    else:
        Profile(**data).save()
    return JsonResponse({"ok": 1})

# 修改密码视图
def change_password(request):
    if not request.user.is_authenticated:
        return error('...')
    try:
        data = simplejson.loads(request.body)
    except:
        data = {}
    
    if data['npassword'] != data['npassword2']:
        return error(message="确认密码不一致")

    if not request.user.check_password(data['password']):
        return error(message="原密码错误")
    # 修改密码
    request.user.set_password(data['npassword'])
    request.user.save() #保存
    # 修改密码后需要重新登陆
    logout(request)
    return success()
