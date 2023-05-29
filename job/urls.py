from django.urls import path
from .views import *

urlpatterns = [
    path('job/', get_jobs), # 分页查询职位信息(前端职位数据表格使用)
    path('recommand/', recommand), # 推荐职位信息
    path('predict/', predict_salary), # 薪资水平预测
    path('job/<jobid>/', get_job), # 获取职位详情
    path('chart/workyear/', workyear_chart), # 工作年限分析视图
    path('chart/workarea/', workarea_chart), # 工作地区分析视图
    path('chart/providesalary/', salary_chart), # 薪资睡拼分析视图
    path('chart/degree/', degree_chart), # 学历水平分析视图
]
