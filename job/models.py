from django.db import models

# Create your models here.
{
    'jobid': '136332590',
    'job_name': '产品经理（停车行业）',
    'job_href': 'https://jobs.51job.com/chongqing-jbq/136332590.html?s=sou_sou_soulb&t=0_0',
    'coid': '6227499',
    'company_name': '百度智行信息科技（重庆）有限公司',
    'company_href': 'https://jobs.51job.com/all/co6227499.html',
    'providesalary_text': '1.5-2.5万/月',
    'workarea': '060300',
    'workarea_text': '重庆-江北区',
    'companytype_text': '上市公司',
    'degreefrom': '6',
    'workyear': '5',
    'jobwelf': '五险一金 专业培训 年终奖金 项目奖金',
    'companysize_text': '50-150人',
    'companyind_text': '计算机软件',
    'workyear_text': '3-4年经验',
    'degreefrom_text': '本科',
    'providesalary_min': 15.0,
    'providesalary_max': 25.0,
    'attribute': '重庆-江北区|3-4年经验|本科|招1人',
    'jobinfo': '<p>1-负责编制停车、自动驾驶、智慧交通领域政府项目规划和设计方案，并推进实施</p><p>2-参与政府规划方案及项目指南编制，支持拓展政府合作项目</p><p>3-拓展、维护与停车、自动驾驶、智能交通政府主管部门及重点地方政府关系</p><p><br></p><p>职位要求:</p><p>1-本科及以上学历，5年以上相关工作经验，有政府、研究机构、互联网工作经验者优先</p><p>2-了解政府项目推进流程，具有和政府部门沟通、合作的经验，掌握一定的政府资源</p><p>3-具有较强的项目方案编制能力</p><p>4-具有强烈的进取心，精力充沛，身体健康，乐观豁达，富有开拓精神</p>'}

# 职位数据模型！！！！！
class Job(models.Model):
    jobid = models.CharField('职位id', max_length=50, unique=True)
    job_name = models.CharField('职位名称', max_length=200)
    job_href = models.TextField('职位原链接', editable=False)
    coid = models.CharField('公司id', max_length=50)
    company_name = models.CharField('公司名称', max_length=200)
    company_href = models.TextField('公司原链接', editable=False)
    providesalary_text = models.TextField('薪资水平')
    workarea = models.CharField('地区编码', max_length=200, editable=False)
    workarea_text = models.CharField('工作地区', max_length=200)
    companytype_text = models.CharField('公司类型', max_length=200)
    degreefrom = models.CharField('学历编码', max_length=200, editable=False)
    degreefrom_text = models.CharField('学历', max_length=200)
    workyear = models.CharField('工作经验编码', max_length=200, editable=False)
    workyear_text = models.CharField('工作经验', max_length=200)
    jobwelf = models.TextField('工作福利')
    companysize_text = models.TextField('公司规模', max_length=200)
    companyind_text = models.TextField('公司行业', max_length=200)
    providesalary_min = models.FloatField('薪资最小值(千/月)', null=True)
    providesalary_max = models.FloatField('薪资最大值(千/月)', null=True)
    attribute = models.TextField('职位属性')
    jobinfo = models.TextField('职位详情')

    def __str__(self):
        return self.job_name

    class Meta:
        db_table = "job"
        verbose_name = "职位"
        verbose_name_plural = "职位"
