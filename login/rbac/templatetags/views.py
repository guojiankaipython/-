from django.shortcuts import render,redirect,HttpResponse,reverse
from django.conf import settings
from django.db.models import Q
from django.views import View
from django.db import transaction
from django.forms import modelformset_factory

import json

from rbac.serve.permission_insert import init_permission




from app01 import forms
from app01 import models
from utils import md5_tool,pager


# Create your views here.

def login(request):
    if request.method == 'GET':

        return render(request, 'auth/login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = models.User.objects.filter(username=username,password=md5_tool.set_md5(password,username))
        if user_obj:
            request.session['is_login'] = True
            request.session['username'] = username
            init_permission(request,username)
            return redirect('home')
        else:
            return render(request, 'auth/login.html', {'errors': '用户名或密码有误！'})
def logout(request):
    """
    注销
    :param request:
    :return:
    """
    request.session.flush()
    return redirect('login')


def register(request):
    if request.method == 'GET':
        user_obj = forms.User()
        return render(request, 'auth/register.html', {'user_obj':user_obj})
    else:
        user_obj = forms.User(request.POST)
        if user_obj.is_valid():
            new_data = user_obj.cleaned_data
            new_data.pop('r_password')
            new_data['password'] = md5_tool.set_md5(new_data['password'],new_data['username'])
            models.User.objects.create(
                **new_data
            )
            return redirect('login')
        else:
            return render(request, 'auth/register.html', {'user_obj':user_obj})
def home(request):
    return render(request, 'home.html')


#客户信息展示，分页展示，点击编辑，保存的原来页面
class Customer(View):

    def get(self,request):
        path = request.path

        current_page_num = request.GET.get('page')
        get_data = request.GET.copy()
        if path == reverse('customers'):
            tags = 1
            all_customers = models.Customer.objects.filter(delete_status=False, consultant__isnull=True).order_by('-id')
        else:
            tags = 2
            all_customers = models.Customer.objects.filter(delete_status=False,consultant__username=request.session.get('username')).order_by('-id')

        select = request.GET.get('select')

        select_way = request.GET.get('select_content')
        if select and select_way:
            q = Q()
            q.children.append([select, select_way])
            all_customers = all_customers.filter(q)
        all_num_count = all_customers.count()
        page_obj = pager.Pagination(current_page_num, all_num_count, get_data, settings.PAGE_NUM_SHOW,settings.DATA_SHOW_NUMBER)
        page_html = page_obj.html()
        all_customers = all_customers[page_obj.start_data_num:page_obj.end_data_num]
        return render(request, 'sales/customers_list.html', {'all_customers': all_customers, 'page_html': page_html, 'tags': tags})

    def post(self,request):
        customers_id = request.POST.get('customers')
        customers_id = json.loads(customers_id)
        bulk_action = request.POST.get('bulk_action')
        if hasattr(self,bulk_action):
            ret = getattr(self,bulk_action)(request,customers_id)
            if ret and customers_id:
                return ret
            else:
                return HttpResponse('无返回值')
    def reverse_gs(self,request,customers_id):

        with transaction.atomic():
            customers = models.Customer.objects.select_for_update().filter(id__in=customers_id)
            msg_list = []
            for cus in customers:
                if cus.consultant:
                    msg_list.append(cus.name)
            msg = ','.join(msg_list)


            models.Customer.objects.filter(id__in=customers_id,consultant__isnull=True).update(
                consultant = models.User.objects.filter(
                    username=request.session.get('username')
                ).first()
            )

        return HttpResponse('公转私'+msg)

    def reverse_sg(self, request, customers):
        models.Customer.objects.filter(id__in=customers).update(
            consultant=None
        )

        return HttpResponse('私转公')



def addEditCustomer(request,customers_id=None):

    obj_list = models.Customer.objects.filter(id=customers_id)
    if request.method == 'GET':
        form_obj = forms.Cusromer(instance=obj_list.first())

        return render(request, 'sales/customer_add.html', {'form_obj':form_obj, 'customers_id':customers_id})

    else:
        next_url = request.GET.get('next')
        form_obj = forms.Cusromer(request.POST,instance=obj_list.first())
        if form_obj.is_valid():
            form_obj.save()
            if customers_id:
                return redirect(next_url)
            else:
                return redirect('customers')
        else:
            return render(request, 'sales/customer_add.html', {'form_obj':form_obj, 'customers_id':customers_id})


def customer_del(request,cid):

    models.Customer.objects.filter(pk=cid).update(
        delete_status=True,
    )
    return redirect('customers')

#跟进信息展示，分页展示，点击编辑之后，保存跳转到原来页面
class FollowUpRecords(View):

    def get(self,request):
        current_page_num = request.GET.get('page')
        get_data = request.GET.copy()

        cid = request.GET.get('cid')
        if cid:
            consult_record_list = models.ConsultRecord.objects.filter(consultant__username=request.session.get('username'),delete_status=False,customer_id=cid)
        else:
            consult_record_list = models.ConsultRecord.objects.filter(consultant__username=request.session.get('username'),delete_status=False,)
        all_num_count = consult_record_list.count()

        page_obj = pager.Pagination(current_page_num,all_num_count,get_data,settings.DATA_SHOW_NUMBER,settings.PAGE_NUM_SHOW)
        page_html = page_obj.html()
        consult_record_list = consult_record_list[page_obj.start_page_num:page_obj.end_data_num]
        return render(request, 'sales/follow_up_records_list.html', {'consult_record_list':consult_record_list, 'page_html':page_html, })


def addEditFollowUpRecords(request,customers_id = None):
    obj_list = models.ConsultRecord.objects.filter(id=customers_id)

    if request.method == 'GET':
        form_obj = forms.ConsultRecord(request,instance=obj_list.first())
        return render(request, 'sales/consult_record_edit.html', {'form_obj':form_obj, 'customers_id':customers_id})

    else:
        next_url = request.GET.get('next')
        form_obj = forms.ConsultRecord(request,request.POST,instance=obj_list.first())
        if form_obj.is_valid():
            form_obj.save()
            if customers_id:
                return redirect(next_url)
            else:
                return redirect('follow_up_records')
        else:
            return render(request, 'sales/consult_record_edit.html', {'form_obj':form_obj, 'customers_id':customers_id})



#报名记录
def enrollments_list(request):
    enrollments_records = models.Enrollment.objects.all()

    return render(request, 'sales/enrollments_list.html', {'enrollments_list':enrollments_records})



#跟进记录删除
def follow_up_records_del(request,customers_id):

    models.ConsultRecord.objects.filter(id=customers_id).update(
        delete_status=True
    )
    return redirect('follow_up_records')

# 课程记录
class CourseRecordList(View):

    def get(self,request):
        course_record_list = models.CourseRecord.objects.all()
        return render(request, 'sales/course_record_list.html', {'course_record_list':course_record_list})

    def post(self,request):
        course_record_id = request.POST.get('course_record')
        course_record_id = json.loads(course_record_id)
        bulk_action = request.POST.get('bulk_action')
        if hasattr(self,bulk_action):
            ret = getattr(self,bulk_action)(request,course_record_id)
            if ret and course_record_id:
                return ret
            else:
                return HttpResponse('无返回值')
    def bulk_create_sr(self,request,course_record_id):
        try:
            with transaction.atomic():
                for course_id in course_record_id:
                    course_obj = models.CourseRecord.objects.filter(id=course_id).first()
                    student_objs = course_obj.re_class.customer_set.filter(status='studying')
                    if student_objs:
                        for student in student_objs:
                            models.StudyRecord.objects.create(
                                course_record_id=course_id,
                                student=student
                            )
                    else:
                        return HttpResponse('失败')

            return HttpResponse('成功')
        except Exception:
            return HttpResponse('失败')

class StudyRecordList(View):

    def get(self,request,cid):

        study_obj = models.StudyRecord.objects.filter(course_record_id=cid)

        form_set = modelformset_factory(models.StudyRecord,forms.StudyRecord,extra=0)
        form_set = form_set(queryset=study_obj)
        # sutdy_objs = models.StudyRecord.objects.filter(course_record_id=course_id)
        return render(request, 'sales/study_record_list.html', {'form_set':form_set})

    def post(self,request,cid):
        form_set = modelformset_factory(models.StudyRecord,forms.StudyRecord,extra=0)
        form_set = form_set(request.POST)

        if form_set.is_valid():
            form_set.save()
            return redirect(request.path)
        else:
            return render(request, 'sales/study_record_list.html', {'form_set': form_set})


