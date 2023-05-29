import re
import scrapy
import json
import requests
from scrapy.shell import inspect_response

# 免费代理ip获取


def get_proxy():
    url = "http://demo.spiderpy.cn/get/"
    d = requests.get(url).json()['proxy']
    return f"http://{d}"

# 工具函数


def get_dict(d):
    r = dict()
    try:
        for i in attrs:
            r[i] = d.get(i)
        r['workyear_text'] = workyear[r['workyear']]
        r['degreefrom_text'] = degrees[r['degreefrom']]
        r['providesalary_min'], r['providesalary_max'] = parse_salary(
            r['providesalary_text'])
        r['attribute'] = "|".join(r['attribute_text'])
        del(r['attribute_text'])
        return r
    except:
        print(r)
        raise

# 文字形式的薪资，转换为数字形式


def parse_salary(stext):
    if stext == '':
        return 0, 0
    try:
        smin, smax, sunit, syear = re.search(
            r"(\d+(?:\.\d+)?)\-(\d+(?:\.\d+)?)(千|万)/(月|年)", stext).groups()
        year = {
            "月": 1,
            "年": 12,
        }
        unit = {
            "千": 1,
            "万": 10,
        }
        smin = float(smin)/year[syear]*unit[sunit]
        smax = float(smax)/year[syear]*unit[sunit]
        return smin, smax
    except:
        print("报错", stext)
        return 0, 0


# 职位数据字段
attrs = (
    'jobid',
    'job_name',
    'job_href',
    'coid',
    'company_name',
    'company_href',
    'providesalary_text',
    'workarea',
    'workarea_text',
    'companytype_text',
    'degreefrom',
    'workyear',
    'jobwelf',
    'attribute_text',
    'companysize_text',
    'companyind_text',
)
# 学历字段映射
degrees = {
    "1": "初中及以下",
    "2": "高中",
    "3": "中技",
    "4": "中专",
    "5": "大专",
    "6": "本科",
    "7": "硕士",
    "8": "博士",
    "": "无学历要求"
}
# 工作年限字段映射
workyear = {
    "1": "在校生/应届生",
    "3": "1年经验",
    "4": "2年经验",
    "5": "3-4年经验",
    "6": "5-7年经验",
    "7": "8-9年经验",
    "8": "10年以上经验",
    "10": "无需经验",
    "": "无需经验",
}

# 爬虫类


class BossSpider(scrapy.Spider):
    name = 'boss'
    allowed_domains = []
    start_urls = []

    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Referer": "https://search.51job.com/list",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4755.0 Safari/537.36",
            "Cookie": "_uab_collina=164015274397611330723552; guid=4c0af13cdd26adcd11f086dbf6f8f8c5; m_search=areacode%3D250200; acw_tc=76b20fed16401527374223128e3093a9601d95f934098daaf63351c39dd2ca; nsearch=jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D; acw_sc__v2=61c2beaaaa4444dc6e6c5369d01ec5aa3855ca1a; search=jobarea%7E%60000000%7C%21ord_field%7E%601%7C%21recentSearch0%7E%60000000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21; ssxmod_itna=QqGxnDg7eGTwDXQG7GTG=LoAKGQGkFK4hUSfIDBwq4iNDnD8x7YDvG+=CGSYS98loP0xFinkaq4LtUm25h1Km+GPYD84i7DKqibDCqD1D3qDki7Dx0rDzw=Gu3NKDYDI401DbqGOhLV3dDYkQDmdp9GTUgDkdDCx+4bEDYffwn97pxIGxPY7GQj0uoQ7DK9B+nI7TTI0Te+A+f+PDA86+NjiD===; ssxmod_itna2=QqGxnDg7eGTwDXQG7GTG=LoAKGQGkFK4hUSID8q6w2eGXF4Ga/I7KmxX7iCvmv62cjG/D3kivhR/ck9XNKM0m0bC4qb1gPO4xn4WITCxFK4OHYVkbupT0P13KOQCoyGOHB7TyP/NnAHHZ=cWc6FsVQT1epAQpp9NzhuhNUrzuBPHrooGaSPGZQpHQeYzm95tG9yEvcwfpI9Ap3SwCgnw0OmHTcTOu70bpgMWdb9EVWvHH8jINIQOD9lDBQw4dxjbV+grrZey=LAQxVZeac78kwMTvy68QxtT3dtg5aVQEd/l56zsk5jSzHOWF2lv/zvc0FG47w0D4rw4=vk7b8iv4wbOGReZP+7el9H4VIyt4Yg9NQiPNb/ByMn7wBYlS5KNBy3E5Ov4hgTbgQ/i5ixDKM4jE5ILdkD5Al5q14PZ5kDEwkAWo7K6q3D=1D51B4eYbVBfB2eBB4EEDgBKA2DD4qP05dfqZlepRK9iolhx2pKu=LD7=DYKxeD="
        }
    }
    headers = {
        # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        # "Cookie": "guid=ff094c57135dc0aec51b5df060accf59; nsearch=jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D; search=jobarea%7E%60000000%7C%21ord_field%7E%600%7C%21; acw_tc=2f624a5c16363549361946180e1880b29ab28a1b7a5d2f2135e943a3089cf3; acw_sc__v2=6188cb78d6e3b294362dcc3073b0534ddb746bea; ssxmod_itna=Yq0xgD9D0DuQqAKY0dD=G7IHewqLKQKa33TYa8Dl1rxA5D8D6DQeGTTRaeIq3r3YDBKai8Ahxh3fQQGxLmiWom0PaoaO3qDIDmKDyDW5DlDDR74YDlP3dTDneGRDQ5G03qGYDbxYERlV4DS+qD9DDPZDYpRDDol3qGwDiUSDDt7S4G2ILQe8EQqx7ESDiQDRLj6fqGc+dbDA8GPax0xojQDzfRB/fQDI4Gy4TRQ1ZcBReIXDIiGxBQWEhyxpC+xFSSoQE5FKOeoYGhW30GqUihRc0EqefGucikBaDDAGiYy7iD==; ssxmod_itna2=Yq0xgD9D0DuQqAKY0dD=G7IHewqLKQKa33TYaD6p/7iD05nPq03aYYn60QHnQcKCgcK1cU7BPx8Hflq2dvKnEBa=DyAkA48D8g4H4Nz2ZM23eZtBBcns5iZcHXHlaxZCUqipjQhjUmWH0cc1QxxOngnQXi7xQ=mNsxxTaa9PW951dEgGTxF+XaOwn1nie+emUZgFzpPAHUBEUtfmgmehXtW=s67ab/8agFd6GRd7Q=iAR8pHd1hR9bCHWF5EsgwcbFZj1ZoWp2jnFsEfpx5gz2lgf3g+rLIg2LZl69cr3HIEHwz/fdVZDYSii3D07Mrxr+diB3Wb40xhrR5QnhiD1=mYdl3gA4eDdiwYTCw90wQhD3DDLxD2jmQKD8fuKPD="
    }

    # url_fmt = "https://search.51job.com/list/000000,000000,0000,00,9,99,+,2,{page}.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare="
    url_fmt = "https://search.51job.com/list/000000,000000,0000,00,9,99,+,2,{page}.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=1&dibiaoid=0&line=&welfare="
    # detail_fmt = "https://jobs.51job.com/jinshuiqu/{jobid}.html?s=sou_sou_soulb&t=0_0"
    # detail_fmt = "https://51rz.51job.com/job.html?jobid={jobid}"
    detail_fmt = "https://msearch.51job.com/jobs/all/{jobid}.html?rc=03"

    def start_requests(self):
        meta = dict(page=1)
        url = self.url_fmt.format(page=meta['page'])
        yield scrapy.Request(url, meta=meta, callback=self.parse)

    def parse(self, response):
        meta = response.meta
        data = json.loads(response.text).get("engine_jds", [])
        for i in data:
            d = get_dict(i)
            meta['data'] = d
            yield scrapy.Request(self.detail_fmt.format(jobid=d['jobid']), meta=meta, callback=self.parse_detail)

        if data:
            meta['page'] += 1
            url = self.url_fmt.format(page=meta['page'])
            yield scrapy.Request(url, meta=meta, callback=self.parse)

    def parse_detail(self, response):
        data = response.meta['data']
        jobinfo = ''.join(response.xpath("//article/*").extract())
        data['jobinfo'] = jobinfo
        if jobinfo:
            yield data
        # inspect_response(response, self)
