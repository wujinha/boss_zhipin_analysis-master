from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'), # 首页
    path('detail/<jobid>/', detail, name='detail'), # 职位详情
    path('login/', login, name='login') # 登录
]
