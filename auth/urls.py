from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_view, name='user_login'), # 登录
    path('logout/', logout_view, name='user_logout'), # 退出登录
    path('signup/', signup, name='user_signup'), # 注册
    path('get_profile/', get_profile), # 获取用户信息
    path('save_profile/', save_profile), # 保存用户信息
    path('change_password/', change_password), # 修改密码
]
