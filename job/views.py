import simplejson
from .models import *
from django.shortcuts import render
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.db.models import Q, Count, Avg, Min, Max
from pyecharts import options as opts
from pyecharts.charts import Pie, Funnel, Bar, Scatter, Line, WordCloud, Map
from django.core.paginator import Paginator
from collections import defaultdict
from index.utils import success, error, redirect
from auth.models import Profile
from pyecharts.options.charts_options import MapItem
from collections import Counter

# Create your views here.

# 薪资范围查询条件
salary_q = {
    '面议': Q(providesalary_max=0) & Q(providesalary_min=0),
    '3K以下': Q(providesalary_max__lte=3) & Q(providesalary_max__gt=0),
    '3-5K': Q(providesalary_max__lte=5) & Q(providesalary_max__gt=3),
    '5-10K': Q(providesalary_max__lte=10) & Q(providesalary_max__gt=5),
    '10-15K': Q(providesalary_max__lte=15) & Q(providesalary_max__gt=10),
    '15-20K': Q(providesalary_max__lte=20) & Q(providesalary_max__gt=15),
    '20-30K': Q(providesalary_max__lte=30) & Q(providesalary_max__gt=20),
    '30-50K': Q(providesalary_max__lte=50) & Q(providesalary_max__gt=30),
    '50K以上': Q(providesalary_max__gt=50)
}

# 工具函数
def to_dict(l):
    def _todict(obj):
        j = {k: v for k, v in obj.__dict__.items() if not k.startswith('_')}
        return j
    return [_todict(i) for i in l]

# 推荐职位视图
def recommand(request):
    # 需要登陆才能访问
    if not request.user.is_authenticated:
        return error('...')
    try:
        data = simplejson.loads(request.body)
    except:
        data = {}
    params = {}
    pagesize = data.get('pagesize', 12)
    page = data.get('page', 1)
    # 找到用户信息
    profile = Profile.objects.filter(userid=request.user.id)
    # 如果存在用户信息，就将用户填写的个人资料作为查询条件，用以筛选职位信息
    if profile:
        profile = profile[0]
        if profile.workarea:
            # 如果用户信息填写了工作地区，将它加入职位筛选条件
            params['workarea_text__icontains'] = profile.workarea
        if profile.workyear:
            # 如果用户信息填写了工作年限，将它加入职位筛选条件
            params['workyear_text'] = profile.workyear
        if profile.job_name:
            # 如果用户信息填写了职位名，将它加入职位筛选条件
            params['job_name__icontains'] = profile.job_name
        if profile.degree:
            # 如果用户信息填写了学历，将它加入职位筛选条件
            params['degreefrom_text'] = profile.degree
    params_q = Q(**params)
    # 筛选职位，并按照职位id倒排
    objs = Job.objects.filter(params_q).order_by('-jobid').all()
    pg = Paginator(objs, pagesize)
    # 分页
    page = pg.page(page)
    # 返回数据
    return JsonResponse({'code': 200, 'content': {
        'total': pg.count,
        'results': to_dict(page.object_list)
    }})

# 薪资水平预测视图
def predict_salary(request):
    try:
        data = simplejson.loads(request.body)
    except:
        data = {}
    not_q = ('total', 'page', 'pagesize', 'providesalary')
    params = {k: v for k, v in data.items() if k not in not_q and v}
    params_q = Q(**params) & Q(providesalary_max__gt=0)
    # 按所给条件查询职位信息，并聚合，算出最低薪资、最高薪资、平均薪资
    data = Job.objects.filter(params_q).aggregate(min=Min(
        'providesalary_min'), max=Max('providesalary_min'), avg=Avg('providesalary_min'))
    # 返回数据
    return JsonResponse(data)

# 职位信息分页查询
def get_jobs(request):
    try:
        data = simplejson.loads(request.body)
    except:
        data = {}
    not_q = ('total', 'page', 'pagesize', 'providesalary')
    pagesize = data.get('pagesize', 12)
    page = data.get('page', 1)
    # 加入筛选条件
    params = {k: v for k, v in data.items() if k not in not_q and v}
    # 薪资范围筛选条件做特别处理
    if 'providesalary' in data and data['providesalary']:
        q = salary_q[data['providesalary']]
        params_q = Q(**params) & q
    # 其余筛选条件直接加入
    else:
        params_q = Q(**params)
    # 筛选职位，并按照职位id倒排
    objs = Job.objects.filter(params_q).order_by('-jobid').all()
    pg = Paginator(objs, pagesize)
    # 分页
    page = pg.page(page)
    # 返回数据
    return JsonResponse({'code': 200, 'content': {
        'total': pg.count,
        'results': to_dict(page.object_list)
    }})

# 获取单个职位详细信息
def get_job(request, jobid):
    # 按所给职位id，查出职位信息并返回
    obj = get_object_or_404(Job, jobid=jobid)
    return JsonResponse(to_dict([obj])[0])

# 工作年限分析图
def workyear_chart(request):
    try:
        data = simplejson.loads(request.body)
    except:
        data = {}
    not_q = ('total', 'page', 'pagesize', 'providesalary')
    # 加入筛选条件
    params = {k: v for k, v in data.items() if k not in not_q and v}
    # 薪资范围筛选条件做特别处理
    if 'providesalary' in data and data['providesalary']:
        q = salary_q[data['providesalary']]
        params_q = Q(**params) & q
    # 其余筛选条件直接加入
    else:
        params_q = Q(**params)

    # 按所给条件查询职位信息，并按id聚合，统计出所有职位信息的工作年限
    data = {i['workyear_text']: i['count'] for i in Job.objects.filter(
        params_q).values('workyear_text').annotate(count=Count('id'))}
    # 用饼图展示统计数据
    c = (
        Pie()
        .add("", list(data.items()), label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts(title="工作经验分析", pos_left="40%"),
                         legend_opts=opts.LegendOpts(type_="scroll", pos_right="80%", orient="vertical"))
    )
    # 返回数据
    return HttpResponse(c.dump_options(), content_type="application/json")

# 工作地区分析图
def workarea_chart(request):
    try:
        data = simplejson.loads(request.body)
    except:
        data = {}
    not_q = ('total', 'page', 'pagesize', 'providesalary')
    # 加入筛选条件
    params = {k: v for k, v in data.items() if k not in not_q and v}
    # 薪资范围筛选条件做特别处理
    if 'providesalary' in data and data['providesalary']:
        q = salary_q[data['providesalary']]
        params_q = Q(**params) & q
    # 其余筛选条件直接加入
    else:
        params_q = Q(**params)
    # 按所给条件查询职位信息，并按id聚合，统计出所有职位信息的工作地区
    data = [(i['workarea_text'], i['count']) for i in Job.objects.filter(params_q).values(
        'workarea_text').annotate(count=Count('id'))]
    total = []
    # 数据预处理
    for i in data:
        city = i[0].split('-')[0]
        total.extend([city]*i[1])
    # 真正统计出每个地区有多少职位
    counter = list(Counter(total).items())
    # 用地图展示统计数据
    m = (
        Map()
        .add("城市", counter, "china-cities",  is_roam=True, is_map_symbol_show=False, label_opts=opts.LabelOpts(is_show=False),)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="工作地区分析"),
            visualmap_opts=opts.VisualMapOpts(),
            legend_opts=opts.LegendOpts(is_show=False),
        )
    )
    # m.render("map_china_cities.html")
    # 返回数据
    return HttpResponse(m.dump_options(), content_type="aplication/text")

# 薪资水平分析图
def salary_chart(request):
    try:
        data = simplejson.loads(request.body)
    except:
        data = {}
    not_q = ('total', 'page', 'pagesize', 'providesalary')
    # 加入筛选条件
    params = {k: v for k, v in data.items() if k not in not_q and v}
    # 薪资范围筛选条件做特别处理
    if 'providesalary' in data and data['providesalary']:
        q = salary_q[data['providesalary']]
        params_q = Q(**params) & q
    # 其余筛选条件直接加入
    else:
        params_q = Q(**params)
    # 拿到所有职位数据的最低薪资与最高薪资
    data = list(Job.objects.filter(params_q).values(
        'providesalary_min', 'providesalary_max'))
    # 进行薪资范围分组
    salary_groups = {
        '面议': lambda i, a: i == 0 and a == 0,
        '3K以下': lambda i, a: 0 < a <= 3,
        '3-5K': lambda i, a: 3 < a <= 5,
        '5-10K': lambda i, a: 5 < a <= 10,
        '10-15K': lambda i, a: 10 < a <= 15,
        '15-20K': lambda i, a: 15 < a <= 20,
        '20-30K': lambda i, a: 20 < a <= 30,
        '30-50K': lambda i, a: 30 < a <= 50,
        '50K以上': lambda i, a: a > 50
    }
    # 统计并将数据进行分组
    counter = defaultdict(int)
    for i in data:
        providesalary_min, providesalary_max = i['providesalary_min'], i['providesalary_max']
        for k, v in salary_groups.items():
            if v(providesalary_min, providesalary_max):
                counter[k] += 1
                break
    # 用柱状图展示统计数据
    c = (
        Bar()
        .add_xaxis([i[0] for i in counter.items()])
        .add_yaxis("", [i[1] for i in counter.items()], label_opts=opts.LabelOpts(is_show=False))
        # .reversal_axis()
        .set_global_opts(
            title_opts=opts.TitleOpts(title="薪资水平分析"),
            # datazoom_opts=opts.DataZoomOpts(orient="vertical"),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                axispointer_opts=opts.AxisPointerOpts(
                    is_show=True, type_="shadow"),
            )
        )
    )
    # 返回数据
    return HttpResponse(c.dump_options(), content_type="application/json")

# 学历分析图
def degree_chart(request):
    try:
        data = simplejson.loads(request.body)
    except:
        data = {}
    not_q = ('total', 'page', 'pagesize', 'providesalary')
    # 加入筛选条件
    params = {k: v for k, v in data.items() if k not in not_q and v}
    # 薪资范围筛选条件做特别处理
    if 'providesalary' in data and data['providesalary']:
        q = salary_q[data['providesalary']]
        params_q = Q(**params) & q
    # 其余筛选条件直接加入
    else:
        params_q = Q(**params)
    # 按所给条件查询职位信息，并按id聚合，统计出不同的学历有多少职位
    data = {i['degreefrom_text']: i['count'] for i in Job.objects.filter(
        params_q).values('degreefrom_text').annotate(count=Count('id'))}
    # 用饼图展示数据
    c = (
        Pie()
        .add("", list(data.items()), label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts(title="学历水平分析", pos_left="40%"),
                         legend_opts=opts.LegendOpts(type_="scroll", pos_right="80%", orient="vertical"))
    )
    # 返回数据
    return HttpResponse(c.dump_options(), content_type="application/json")
