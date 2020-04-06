from django.shortcuts import render,HttpResponse,redirect
from django import forms
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.forms import modelformset_factory,formset_factory

from app01.models import User

from rbac.myform import MultiPermissionForm
from rbac import models
from rbac.serve.routes import get_all_url_dict
from rbac.serve.icons import icon_list

class RoleModelForm(forms.ModelForm):

    class Meta:
        model = models.Role
        fields = "__all__"
        exclude = ['permissions',]

        labels = {
            'role_name':'角色',
        }
        widgets = {
            'role_name':forms.TextInput(attrs={'class':'form-control'})
        }




class MenuModelForm(forms.ModelForm):

    class Meta:
        model = models.Menu
        fields = "__all__"

        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'weight':forms.TextInput(attrs={'class':'form-control'}),
            'icon':forms.RadioSelect(choices=[(i[0],mark_safe(i[1])) for i in icon_list]),
            }


class PermissionModelForm(forms.ModelForm):

    class Meta:
        model = models.Permission
        fields = "__all__"

        widgets = {
            'url':forms.TextInput(attrs={'class':'form-control'}),
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'icon':forms.TextInput(attrs={'class':'form-control'}),
            'menu':forms.TextInput(attrs={'class':'form-control'}),
            'url_name':forms.TextInput(attrs={'class':'form-control'}),
            'parent':forms.TextInput(attrs={'class':'form-control'}),
        }

def role_list(request):

    role_lists = models.Role.objects.all()
    return render(request,'rbac/role_list.html',{'role_lists':role_lists})

def role_add_edit(request,role_id=None):
    role_objs = models.Role.objects.filter(id=role_id).first()
    if request.method == 'GET':

        form = RoleModelForm(instance=role_objs)
        return render(request,'rbac/role_add.html',{'form':form})
    else:
        form = RoleModelForm(request.POST,instance=role_objs)
        if form.is_valid():
            form.save()
            return redirect('rbac:role_list')





def role_del(request,role_id):

    models.Role.objects.filter(id=role_id).delete()
    return redirect('rbac:role_list')


def menu_list(request):
    mid = request.GET.get('mid')
    if mid:
        permissions_list = models.Permission.objects.filter(Q(id=mid)|Q(parent__menu_id=mid))
    else:
        permissions_list = models.Permission.objects.all().values()
    permissions_dict = {}
    for permission in permissions_list:
        mid = permission.get('menu_id')
        if mid:
            permissions_dict[permission['id']] = permission
            permissions_dict[permission['id']]['children'] = []
    for node in permissions_list:
        pid = node.get('parent_id')
        if pid:
            permissions_dict[pid]['children'].append(node)
    menu_lists = models.Menu.objects.all()
    return render(request, 'rbac/menu_list.html',{'menu_lists': menu_lists, 'permissions_dict': permissions_dict, 'mid': mid})



def menu_edit_add(request,menu_id=None):
    menu_objs = models.Menu.objects.filter(id=menu_id).first()
    if request.method == 'GET':
        form = MenuModelForm(instance=menu_objs)
        return render(request,'rbac/menu_edit_add.html',{'form':form})
    else:
        form = MenuModelForm(request.POST,instance=menu_objs)
        if form.is_valid():
            form.save()
            return redirect('rbac:menu_list')
        else:
            return render(request, 'rbac/menu_edit_add.html', {'form': form})



def menu_del(request,menu_id):
    models.Menu.objects.filter(id=menu_id).delete()
    return redirect('rbac:menu_list')



def permissions_edit_add(request,permission_id=None):

    permission_objs = models.Permission.objects.filter(id=permission_id).first()
    if request.method == 'GET':
        form = PermissionModelForm(instance=permission_objs)
        return render(request,'rbac/permission_edit_add.html',{'form':form})
    else:
        form = PermissionModelForm(request.POST,instance=permission_objs)
        if form.is_valid():
            form.save()
            return redirect('rbac:menu_list')
        else:
            return render(request, 'rbac/permission_edit_add.html', {'form': form})

def permissions_del(request,permission_id):
    models.Permission.objects.filter(id=permission_id).delete()
    return redirect('rbac:menu_list')



def multi_permissions(request):
    """
    批量操作权限
    :param request:
    :return:
    """

    post_type = request.GET.get('type')  #add

    # 更新和编辑用的
    FormSet = modelformset_factory(models.Permission, MultiPermissionForm, extra=0)


    # 增加用的
    AddFormSet = formset_factory(MultiPermissionForm, extra=0)

    # 获取数据库中现有的所有权限数据
    permissions = models.Permission.objects.all()

    # 获取项目的路由系统中所有URL
    router_dict = get_all_url_dict(ignore_namespace_list=['admin', ])
    #{'':{'name':'','url'}}

    # 数据库中的所有权限的别名
    permissions_name_set = set([i.url_name for i in permissions])

    # 路由系统中的所有权限的别名
    router_name_set = set(router_dict.keys())



    if request.method == 'POST' and post_type == 'add':
        add_formset = AddFormSet(request.POST)
        if add_formset.is_valid():
            permission_obj_list = [models.Permission(**i) for i in add_formset.cleaned_data]

            query_list = models.Permission.objects.bulk_create(permission_obj_list)

            for i in query_list:
                permissions_name_set.add(i.url_name)

    add_name_set = router_name_set - permissions_name_set  #要新增的那些别名
    add_formset = AddFormSet(initial=[row for name, row in router_dict.items() if name in add_name_set])  #{'url_name':'','url'}
    # {'':{'name':'','url'}}

    del_name_set = permissions_name_set - router_name_set
    del_formset = FormSet(queryset=models.Permission.objects.filter(url_name__in=del_name_set))

    update_name_set = permissions_name_set & router_name_set

    update_formset = FormSet(queryset=models.Permission.objects.filter(url_name__in=update_name_set))

    if request.method == 'POST' and post_type == 'update':
        update_formset = FormSet(request.POST)
        if update_formset.is_valid():
            update_formset.save()
            update_formset = FormSet(queryset=models.Permission.objects.filter(url_name__in=update_name_set))

    return render(
        request,
        'rbac/multi_permissions.html',
        {
            'del_formset': del_formset,
            'update_formset': update_formset,
            'add_formset': add_formset,
        }
    )


def distribute_permissions(request):
    """
    分配权限
    :param request:
    :return:
    """

    uid = request.GET.get('uid')
    rid = request.GET.get('rid')

    if request.method == 'POST' and request.POST.get('postType') == 'role':
        user = User.objects.filter(id=uid).first()
        if not user:
            return HttpResponse('用户不存在')  # 1  2
            # 1  3
        user.roles.set(request.POST.getlist('roles'))  # [2,3]

    if request.method == 'POST' and request.POST.get('postType') == 'permission' and rid:
        role = models.Role.objects.filter(id=rid).first()
        if not role:
            return HttpResponse('角色不存在')
        role.permissions.set(request.POST.getlist('permissions'))

    # 所有用户
    user_list = User.objects.all()
    user_has_roles = User.objects.filter(id=uid).values('id', 'roles')

    '''
        {}

    '''
    # print('xxxxxxx',user_list)
    # print(user_has_roles)

    user_has_roles_dict = {item['roles']: None for item in user_has_roles}
    # {'角色id':None,}

    """
    用户拥有的角色id
    user_has_roles_dict = { 角色id：None }
    """

    role_list = models.Role.objects.all()
    if rid:
        role_has_permissions = models.Role.objects.filter(id=rid).values('id', 'permissions')
    elif uid and not rid:
        user = User.objects.filter(id=uid).first()
        if not user:
            return HttpResponse('用户不存在')
        role_has_permissions = user.roles.values('id', 'permissions')

    else:
        role_has_permissions = []


    role_has_permissions_dict = {item['permissions']: None for item in role_has_permissions}



    all_menu_list = []
    '''
        [
            {'id':1,'title':'业务管理','children':[

                {'id':1,title:'客户展示','menu_id':1,'children':[
                    {'id':2,'title':'客户添加','parent_id':1}
                ]}

            ]},
            {'id':2,'title':'财务管理','children':[
                {'id':5,title:'缴费展示','menu_id':2,'children':[]}
            ]},
            {'id': None, 'title': '其他', 'children': [
                {'id':9,'title':'嘻嘻嘻',parent_id:None}
            ]}
        ]

    '''

    queryset = models.Menu.objects.values('id', 'title')
    '''
        queryset<[{'id':1,'title':'业务管理','children':[]},]>
    '''
    menu_dict = {}
    '''
        {
            1:{'id':1,'title':'业务管理','children':[

                {'id':1,title:'客户展示','menu_id':1,'children':[]}
            ]},
            2:{'id':2,'title':'财务管理','children':[
                {'id':5,title:'缴费展示','menu_id':2,'children':[]}
            ]},
            None:{'id': None, 'title': '其他', 'children': [
                {'id':9,'title':'嘻嘻嘻',parent_id:None}
            ]},
        }
    '''

    for item in queryset:
        item['children'] = []  # 放二级菜单，父权限
        menu_dict[item['id']] = item
        all_menu_list.append(item)

    other = {'id': None, 'title': '其他', 'children': []}
    all_menu_list.append(other)
    menu_dict[None] = other

    root_permission = models.Permission.objects.filter(menu__isnull=False).values('id', 'title', 'menu_id')  # 二级菜单权限
    '''
        queryset<[{'id':1,title:'客户展示','menu_id':1,'children':[]},]>
    '''
    root_permission_dict = {}
    '''
        {
            二级菜单权限id
            1:{'id':1,title:'客户展示','menu_id':1,'children':[
                {'id':2,'title':'客户添加','parent_id':1}
            ]},
            5:{'id':5,title:'缴费展示','menu_id':2,'children':[]},
        }
    '''

    for per in root_permission:
        per['children'] = []  # 放子权限
        nid = per['id']  # 二级菜单权限id
        menu_id = per['menu_id']  # 一级菜单权限id
        root_permission_dict[nid] = per
        menu_dict[menu_id]['children'].append(per)

    node_permission = models.Permission.objects.filter(menu__isnull=True).values('id', 'title', 'parent_id')  # 二级菜单子权限
    '''
        queryset<[{'id':2,'title':'客户添加','parent_id':1},{'id':9,'title':'嘻嘻嘻',parent_id:None}]>
    '''
    for per in node_permission:
        pid = per['parent_id']
        if not pid:
            menu_dict[None]['children'].append(per)
            continue
        root_permission_dict[pid]['children'].append(per)

    return render(
        request,
        'rbac/distribute_permissions.html',
        {
            'user_list': user_list,
            'role_list': role_list,
            'user_has_roles_dict': user_has_roles_dict,
            'role_has_permissions_dict': role_has_permissions_dict,
            'all_menu_list': all_menu_list,
            'uid': uid,
            'rid': rid
        }
    )



