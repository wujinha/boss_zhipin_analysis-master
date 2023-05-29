from django.db import models

# Create your models here.

# 用户信息数据表
class Profile(models.Model):
    # {
    #     name: null,
    #     degree: null,
    #     workyear: null,
    #     workarea: null,
    #     job_name: null,
    # }
    userid = models.IntegerField(unique=True) # 与用户id相关连
    name = models.TextField(null=True) # 姓名
    degree = models.TextField(null=True) # 学历
    workyear = models.TextField(null=True) # 工作年限
    workarea = models.TextField(null=True) # 工作地点
    job_name = models.TextField(null=True) # 期望职位
