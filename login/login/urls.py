"""login URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from rbac.templatetags import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),

    # 首页
    url(r'^home/$', views.home, name='home'),

    # 公户管理
    url(r'^customers/$', views.Customer.as_view(), name='customers'),

    # 我的客户
    url(r'^mycustomers/$', views.Customer.as_view(), name='mycustomers'),

    #添加用户
    url(r'^customers/add/$', views.addEditCustomer, name='customer_add'),

    # 编辑用户
    url(r'^customers/edit/(\d+)/$', views.addEditCustomer, name='customer_edit'),

    #删除客户
    url(r'^customers/delete/(\d+)/$', views.customer_del, name='customer_del'),

    # 跟进记录
    url(r'^customers/follow_up_records/$', views.FollowUpRecords.as_view(), name='follow_up_records'),

    # 添加跟进记录
    url(r'^consultant/records/add/$', views.addEditFollowUpRecords, name='consultant_records_add'),

    #编辑跟进记录
    url(r'^customers/follow_up_records/edit/(\d+)$', views.addEditFollowUpRecords, name='follow_up_records_edit'),

    # 删除跟进记录
    url(r'^customers/follow_up_records/delete/(\d+)$', views.follow_up_records_del, name='follow_up_records_del'),

    # 报名记录
    url(r'^enrollments/list/$', views.enrollments_list, name='enrollments_list'),

    # 课程记录
    url(r'^course/record/list/$', views.CourseRecordList.as_view(), name='course_record_list'),

    # 学习记录
    url(r'^study/record/list/(\d+)$', views.StudyRecordList.as_view(), name='study_record'),
    # url(r'^study/record/list/$', views.StudyRecordList.as_view(), name='study_record'),

    #注销
    url(r'^logout/$', views.logout, name='logout'),

    #路由分发
    url('^rbac/',include('rbac.urls',namespace='rbac')),

]
