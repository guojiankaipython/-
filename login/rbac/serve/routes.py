from django.conf import settings
from django.utils.module_loading import import_string
from django.urls import RegexURLResolver, RegexURLPattern
from collections import OrderedDict


def recursion_urls(pre_namespace, pre_url, urlpatterns, url_ordered_dict):
    '''

    :param pre_namespace:  None   'rbac'
    :param pre_url:   '/'   '/^rbac/'
    :param urlpatterns:
            [
            # /rbac/role/list

            url(r'^role/list/', views.role_list,name='role_list'),
            url(r'^role/add/', views.role_add_edit,name='role_add'),
            url(r'^role/edit/(\d+)/', views.role_add_edit,name='role_edit'),
            url(r'^role/del/(\d+)/', views.role_del,name='role_del'),

        # 菜单相关
        url(r'^menu/list/', views.menu_list,name='menu_list'),
        url(r'^menu/add/', views.menu_add_edit,name='menu_add'),
        url(r'^menu/edit/(\d+)/', views.menu_add_edit,name='menu_edit'),

        #批量操作权限
        url(r'^multi/permissions/$', views.multi_permissions, name='multi_permissions'),

        ]
        [

            url(r'^', include('web.urls')),
            url(r'^rbac/', include('rbac.urls',namespace='rbac')),
            url(r'^xxx/', views.xxx,name='xxx'),

        ]
    :param url_ordered_dict:   {} {}
    :return:
    '''

    for item in urlpatterns:
        if isinstance(item, RegexURLResolver):
            if pre_namespace:
                if item.namespace:
                    namespace = "%s:%s" % (pre_namespace, item.namespace,)
                else:
                    namespace = pre_namespace
            else:
                if item.namespace:  #'rbac'
                    namespace = item.namespace
                else:
                    namespace = None
                    # '/^rbac/'
            recursion_urls(namespace, pre_url + item.regex.pattern, item.url_patterns, url_ordered_dict)
        else:

            if pre_namespace:  #'rbac'
                name = "%s:%s" % (pre_namespace, item.name,) #rbac:role_list
            else:
                name = item.name  #'xxx'
            if not item.name:
                raise Exception('URL路由中必须设置name属性')

            url = pre_url + item._regex   #'/xxx/' = '/^^login/$'
            url_ordered_dict[name] = {'url_name': name, 'url': url.replace('^', '').replace('$', '')}



            # reverse('login') -- '/login/'
            # {'login':{'name':'login','url':'/login/'},{'rbac:role_list':{'name':'rbac:role_list',url:'/rbac/role/list/'}}}


def get_all_url_dict(ignore_namespace_list=None):
    """
    获取路由中
    :return:
    """
    ignore_list = ignore_namespace_list or [] #短路操作 ['admin',]
    url_ordered_dict = OrderedDict()  #有序字典,最终要使用的字典数据


    md = import_string(settings.ROOT_URLCONF)
    # md = import_string('luffy_permission.urls')

    urlpatterns = []
    '''
        [
            
            url(r'^', include('web.urls')),
            url(r'^rbac/', include('rbac.urls',namespace='rbac')),
            url(r'^xxx/', views.xxx,name='xxx'),
            
        ]
    '''

    '''
        [
            url(r'^admin/', admin.site.urls),
            url(r'^', include('web.urls')),
            url(r'^rbac/', include('rbac.urls',namespace='rbac')),
            url(r'^xxx/', views.xxx,name='xxx'),
        ]
        [<RegexURLResolver <RegexURLPattern list> (admin:admin) ^admin/>,
         <RegexURLResolver <module 'web.urls' from 'D:\\26crm_project\\luffy_permission-最初板\\web\\urls.py'> (None:None) ^>, 
         <RegexURLResolver <module 'rbac.urls' from 'D:\\26crm_project\\luffy_permission-最初板\\rbac\\urls.py'> (None:rbac) ^rbac/>
         <RegexURLPattern xxx ^xxx/>
         ]
        
    '''
    for item in md.urlpatterns:
        if isinstance(item, RegexURLResolver) and item.namespace in ignore_list:
            continue
        urlpatterns.append(item)

    recursion_urls(None, "/", urlpatterns, url_ordered_dict)
    return url_ordered_dict
