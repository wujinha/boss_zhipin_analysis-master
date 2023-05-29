# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'boss_zhipin_analysis.settings')
django.setup()

# 工具函数
def get_fields(model_cls):
    return [i.name for i in model_cls._meta.fields if i.name != 'id']

# 工具函数
def load_dict(model_cls, item):
    fields = get_fields(model_cls)
    return {k: v for k, v in item.items() if k in fields}

# 数据入库中间件
class BossZhipinSpiderPipeline:
    def process_item(self, item, spider):
        from job.models import Job
        try:
            data = load_dict(Job, item)
            Job.objects.create(**data)
            print(data['job_name'], data['company_name'])
        except Exception as e:
            print(e)
