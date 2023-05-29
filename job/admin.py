from django.contrib import admin
from .models import *
from django.utils.html import format_html

# 后台职位管理配置
class JobAdmin(admin.ModelAdmin):
    list_display = (
        # 'jobid',
        'job_name',
        # 'job_href',
        # 'coid',
        'company_name',
        # 'company_href',
        'providesalary_text',
        # 'workarea',
        'workarea_text',
        'companytype_text',
        # 'degreefrom',
        # 'workyear',
        'jobwelf',
        'companysize_text',
        'companyind_text',
        'workyear_text',
        'degreefrom_text',
        # 'providesalary_min',
        # 'providesalary_max',
        'attribute',
        # 'jobinfo'
    )
    list_display_links = ('job_name',)
    list_filter = ('companytype_text', 'workyear_text',
                   'companysize_text', 'degreefrom_text')
    list_select_related = True
    list_per_page = 20
    list_max_show_all = 200
    list_editable = ()
    search_fields = ('job_name', 'company_name')
    date_hierarchy = None
    save_as = False
    save_as_continue = True
    save_on_top = False
    preserve_filters = True
    inlines = []

    def image(self, obj):
        return format_html('<img src="{cover}" width=300 height=200>', cover=obj.imageUrl)
    image.short_description = '图片'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Job, JobAdmin)
admin.site.site_title = "招聘信息后台"
admin.site.site_header = admin.site.site_title
