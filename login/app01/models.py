from django.db import models
from rbac.models import Userinfo

# Create your models here.

from multiselectfield import MultiSelectField

course_choices = (('LinuxL', 'Linux中高级'),
                  ('PythonFullStack', 'Python高级全栈开发'),)

class_type_choices = (('fulltime', '脱产班',),
                      ('online', '网络班'),
                      ('weekend', '周末班',),)

source_type = (('qq', "qq群"),
               ('referral', "内部转介绍"),
               ('website', "官方网站"),
               ('baidu_ads', "百度推广"),
               ('office_direct', "直接上门"),
               ('WoM', "口碑"),
               ('public_class', "公开课"),
               ('website_luffy', "路飞官网"),
               ('others', "其它"),)

enroll_status_choices = (('signed', "已报名"),
                         ('unregistered', "未报名"),
                         ('studying', '学习中'),
                         ('paid_in_full', "学费已交齐"))

seek_status_choices = (('A', '近期无报名计划'), ('B', '1个月内报名'), ('C', '2周内报名'), ('D', '1周内报名'),
                       ('E', '定金'), ('F', '到班'), ('G', '全款'), ('H', '无效'),)
pay_type_choices = (('deposit', "订金/报名费"),
                    ('tuition', "学费"),
                    ('transfer', "转班"),
                    ('dropout', "退学"),
                    ('refund', "退款"),)

attendance_choices = (('checked', "已签到"),
                      ('vacate', "请假"),
                      ('late', "迟到"),
                      ('absence', "缺勤"),
                      ('leave_early', "早退"),)

score_choices = ((100, 'A+'),
                 (90, 'A'),
                 (85, 'B+'),
                 (80, 'B'),
                 (70, 'B-'),
                 (60, 'C+'),
                 (50, 'C'),
                 (40, 'C-'),
                 (0, ' D'),
                 (-1, 'N/A'),
                 (-100, 'COPY'),
                 (-1000, 'FAIL'),)

class User(Userinfo):
    username = models.CharField(max_length=32,unique=True)
    password = models.CharField(max_length=32)
    telephone = models.CharField(max_length=11,db_index=True)
    #db_index添加索引
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    #1----True   2---False
    def __str__(self):
        return self.username

class Customer(models.Model):
    """
    客户表（销售重点关注对象）
    """
    qq = models.CharField(verbose_name='QQ',max_length=64,unique=True,help_text='QQ号必须唯一')
    #help_text 是在django自带admin中的提示信息，verbose_name是相当于前端页面的label标签的内容

    qq_name = models.CharField('QQ昵称',max_length=64,null=True,blank=True)
    # modelfrom---forms.chioseField(chioses=sex_type,)

    name = models.CharField('姓名',max_length=64,help_text='学员报名后，请更改真实姓名')

    sex_type = (('male','男'),('female','女'))
    sex = models.CharField('性别',choices=sex_type,max_length=16,default='male',blank=True,null=True)

    birthday = models.DateField('出生日期',default=None,help_text='格式yyyy-mm-dd',blank=True,null=True)
    phone = models.CharField('手机号',blank=True,max_length=11,null=True)
    source = models.CharField('客户来源',max_length=64,choices=source_type,default='qq')

    introduce_from = models.ForeignKey('self',verbose_name='转自学员介绍',blank=True,null=True,on_delete=models.CASCADE)
    #self指的就是自己这个表，和下面写法是一样的效果，自关联

    # id  name introduce_from
    # 1   dz   None
    # 2   xf   1
    # 3   cg   1
    course = MultiSelectField('咨询课程',choices=course_choices)  #多选，并且存成一个列表的格式，通过modelform会成为多选框
    class_type = models.CharField('班级类型',max_length=64,choices=class_type_choices,default='fulltime')
    customer_note = models.TextField('客户备注',blank=True,null=True)
    status = models.CharField('状态',choices=enroll_status_choices,null=True,max_length=64,default="unregistered",help_text="选择客户此时的状态")

    date = models.DateField(auto_now_add=True)
    last_consult_date = models.DateField('最后跟进日期',auto_now_add=True)
    next_date = models.DateField('预计再次跟进日期',auto_now_add=True,)


    consultant = models.ForeignKey('User',verbose_name='销售',blank=True,null=True,on_delete=models.CASCADE)

    #一个客户可以报多个班，报个脱产，再报个周末，所以是多对多
    class_list = models.ManyToManyField('ClassList',verbose_name='已报班级',blank=True)

    delete_status = models.BooleanField(default=False)

    class Meta:
        ordering = ['id',]
        verbose_name = '客户信息表'
        verbose_name_plural = '客户信息表'

    def __str__(self):
        return self.name


class Campuss(models.Model):
    """
    校区表
    """
    name = models.CharField('校区',max_length=64)
    address = models.CharField('详细地址',max_length=512,blank=True,null=True)

    def __str__(self):
        return self.name


class ClassList(models.Model):
    """
    班级表
    """
    course = models.CharField('课程名称',max_length=64,choices=course_choices)
    semester = models.IntegerField('学期')
    campuses = models.ForeignKey('Campuss',verbose_name='校区',on_delete=models.CASCADE)
    price = models.IntegerField('学费',default=20000)

    memo = models.CharField('说明',blank=True,null=True,max_length=100)

    start_date = models.DateField("开班日期")

    graduate_date = models.DateField('结业日期',blank=True,null=True)

    # contract = models.ForeignKey('ContractTemplate', verbose_name="选择合同模版", blank=True, null=True,on_delete=models.CASCADE)
    teachers = models.ManyToManyField('User',verbose_name='老师')

    class_type = models.CharField(choices=class_type_choices,max_length=64,verbose_name='班级类型')

    class Mate:
        unqiue_together = ('course','semester','campuses')

    def __str__(self):
        return "{}{}({})".format(self.get_course_display(),self.semester,self.campuses)


class ConsultRecord(models.Model):
    """
    跟进记录表
    """
    customer = models.ForeignKey('Customer', verbose_name="所咨询客户")
    note = models.TextField(verbose_name="跟进内容...")
    status = models.CharField("跟进状态", max_length=8, choices=seek_status_choices, help_text="选择客户此时的状态")
    consultant = models.ForeignKey("User", verbose_name="跟进人")
    date = models.DateTimeField("跟进日期", auto_now_add=True)
    delete_status = models.BooleanField(verbose_name='删除状态', default=False)


class Enrollment(models.Model):
    """
    报名表
    """
    why_us = models.TextField("为什么报名", max_length=1024, default=None, blank=True, null=True)
    your_expectation = models.TextField("学完想达到的具体期望", max_length=1024, blank=True, null=True)
    # contract_agreed = models.BooleanField("我已认真阅读完培训协议并同意全部协议内容", default=False)

    contract_approved = models.BooleanField("审批通过", help_text="在审阅完学员的资料无误后勾选此项,合同即生效", default=False)
    enrolled_date = models.DateTimeField(auto_now_add=True, verbose_name="报名日期")
    memo = models.TextField('备注', blank=True, null=True)
    delete_status = models.BooleanField(verbose_name='删除状态', default=False)
    customer = models.ForeignKey('Customer', verbose_name='客户名称')
    school = models.ForeignKey('Campuss')
    enrolment_class = models.ForeignKey("ClassList", verbose_name="所报班级")

    class Meta:
        unique_together = ('enrolment_class', 'customer')

    def __str__(self):
        return self.customer.name


class CourseRecord(models.Model):
    """课程记录表"""
    day_num = models.IntegerField("节次", help_text="此处填写第几节课或第几天课程...,必须为数字")
    date = models.DateField(auto_now_add=True, verbose_name="上课日期")
    course_title = models.CharField('本节课程标题', max_length=64, blank=True, null=True)
    course_memo = models.TextField('本节课程内容', max_length=300, blank=True, null=True)
    has_homework = models.BooleanField(default=True, verbose_name="本节有作业")
    homework_title = models.CharField('本节作业标题', max_length=64, blank=True, null=True)
    homework_memo = models.TextField('作业描述', max_length=500, blank=True, null=True)
    scoring_point = models.TextField('得分点', max_length=300, blank=True, null=True)

    re_class = models.ForeignKey('ClassList', verbose_name="班级")
    teacher = models.ForeignKey('User', verbose_name="讲师")

    class Meta:
        unique_together = ('re_class', 'day_num')
    def __str__(self):

        return str(self.day_num)



class StudyRecord(models.Model):
    """
    学习记录
    """
    attendance = models.CharField("考勤", choices=attendance_choices, default="checked", max_length=64)
    score = models.IntegerField("本节成绩", choices=score_choices, default=-1)
    homework_note = models.CharField(max_length=255, verbose_name='作业批语', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    note = models.CharField("备注", max_length=255, blank=True, null=True)
    homework = models.FileField(verbose_name='作业文件', blank=True, null=True, default=None)
    course_record = models.ForeignKey('CourseRecord', verbose_name="某节课程")
    student = models.ForeignKey('Customer', verbose_name="学员")

    class Meta:
        unique_together = ('course_record', 'student')

    def __str__(self):
        return self.student.name +':'+ str(self.course_record.day_num)

