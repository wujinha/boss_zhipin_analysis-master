const template = `<div style="padding:20px;">
<el-form v-model="queryForm" :inline="true" size="mini">
<el-form-item label="职位名称">
    <el-input v-model="queryForm.job_name__icontains" style="max-width: 300px;" clearable
        @change="queryForm.page=1;doSearch()">
    </el-input>
</el-form-item>
<el-form-item label="工作地区">
    <el-input v-model="queryForm.workarea_text__icontains" style="max-width: 300px;" clearable
        @change="queryForm.page=1;doSearch()">
    </el-input>
</el-form-item>
<el-form-item label="工作福利">
    <el-input v-model="queryForm.jobwelf__icontains" style="max-width: 300px;" clearable
        @change="queryForm.page=1;doSearch()">
    </el-input>
</el-form-item>
<el-form-item label="工作经验">
    <el-select v-model="queryForm.workyear_text" style="max-width: 300px;" clearable
        @change="queryForm.page=1;doSearch()">
        <el-option v-for="value in workyear" :key="value" :value="value" :label="value"></el-option>
    </el-select>
</el-form-item>
<el-form-item label="学历要求">
    <el-select v-model="queryForm.degreefrom_text" style="max-width: 300px;" clearable
        @change="queryForm.page=1;doSearch()">
        <el-option v-for="value in degree" :key="value" :value="value" :label="value"></el-option>
    </el-select>
</el-form-item>
<el-form-item label="薪资范围">
    <el-select v-model="queryForm.providesalary" style="max-width: 300px;" clearable
        @change="queryForm.page=1;doSearch()">
        <el-option v-for="value in salary" :key="value" :value="value" :label="value"></el-option>
    </el-select>
</el-form-item>
<el-form-item>
    <el-button type="primary" @click="queryForm.page=1;doSearch()">搜索</el-button>
</el-form-item>
</el-form>
<el-card shadow="hover" style="margin-top:10px;cursor: pointer;" v-for="job in records"
:key="job.jobid" @click.native="viewDetail(job.jobid)">
<el-row type="flex" justify="space-between" style="margin-bottom: 10px;">
    <el-col :span="8">
        <el-link type="primary" :underline="false" style="font-size: 17px;">{{job.job_name}}
        </el-link>
    </el-col>
    <el-col :span="8">
        <el-link type="primary" :underline="false" style="font-size: 17px;">{{job.company_name}}
        </el-link>
    </el-col>
</el-row>
<el-row type="flex" justify="space-between" style="margin-bottom: 10px;">
    <el-col :span="10">
        <span
            style="font-size:16px;color:darksalmon;margin-right:10px;">{{job.providesalary_text || '面议'}}</span>
        <span style="color:#61687c">{{job.attribute}}</span>
    </el-col>
    <el-col :span="8">
        <span style="color:#61687c;margin-right:5px;">{{job.companytype_text}}</span>
        <span style="color:#61687c">{{job.companysize_text}}</span>
    </el-col>
</el-row>
<el-row type="flex" justify="space-between" style="margin-bottom: 5px;">
    <el-col :span="10">
        <el-tag v-for="welf in job.jobwelf.split(' ')" :key="welf" style="margin:0 5px 5px 0;" @click.stop="queryForm.jobwelf__icontains=welf;queryForm.page=1;doSearch()"
            size="mini" type="info" plain v-show="welf">
            {{welf}}</el-tag>
    </el-col>
    <el-col :span="8">
        <span style="color:#61687c">{{job.companyind_text}}</span>
    </el-col>
</el-row>
</el-card>
<el-row type="flex" justify="center" style="margin-top:20px">
<el-pagination @current-change="handleCurrentChange" :current-page="queryForm.page"
    :page-size="queryForm.pagesize" layout="prev, pager, next, jumper, total"
    :total="queryForm.total" background>
</el-pagination>
</el-row>
</div>
`
var TableView = {
    template,
    data() {
        return {
            queryForm: {
                jobwelf__icontains:null,
                job_name__icontains: null,
                company_name__icontains: null,
                workarea_text__icontains: null,
                workyear_text: null,
                degreefrom_text: null,
                providesalary: null,
                total: 0,
                page: 1,
                pagesize: 12
            },
            records: [],
            salary: ["面议", "3K以下", "3-5K", "5-10K", "10-15K", "15-20K", "20-30K", "30-50K", "50K以上"],
            degree: {
                "1": "初中及以下",
                "2": "高中",
                "3": "中技",
                "4": "中专",
                "5": "大专",
                "6": "本科",
                "7": "硕士",
                "8": "博士",
                "": "无学历要求"
            },
            workyear: {
                "1": "在校生/应届生",
                "3": "1年经验",
                "4": "2年经验",
                "5": "3-4年经验",
                "6": "5-7年经验",
                "7": "8-9年经验",
                "8": "10年以上经验",
                "10": "无需经验",
            },
        }
    },
    beforeMount() {
        this.doSearch()
    },
    methods: {
        viewDetail(jobid) {
            window.open(`/detail/${jobid}`)
        },
        handleClick() {
            this.doSearch()
        },
        handleCommand(cmd) {
            if (cmd === 'gotoAdmin') {
                window.location.href = "/admin"
            } else if (cmd === 'logout') {
                window.location.href = "/user/logout"
            }
        },
        doSearch() {
            axios.post('/ajax/job/', this.queryForm).then(res => {
                this.records = res.data.content.results
                this.queryForm.total = res.data.content.total
            })
        },
        handleCurrentChange(page) {
            this.queryForm.page = page
            this.doSearch()
        }
    },
}