from django.conf import settings
from rbac import models

def init_permission(request,uname):
    """
    权限注入函数
    :param request:  request对象
    :param uname:     用户名称
    :return:
    """
    permission_list = models.Role.objects.filter(user__username=uname).values(
        'permissions__id',
        'permissions__url',
        'permissions__title',
        'permissions__icon',
        'permissions__url_name',
        'permissions__menu_id',
        'permissions__menu__weight',
        'permissions__menu__title',
        'permissions__menu__icon',
        'permissions__parent_id',
    ).distinct()
    menu_dict = {}

    for permission in permission_list:
        if permission['permissions__menu_id']:
            if menu_dict.get(permission['permissions__menu_id']):
                menu_dict[permission['permissions__menu_id']]['children'].append(
                    {
                        'title': permission['permissions__title'],
                        'icon': permission['permissions__icon'],
                        'url': permission['permissions__url'],
                        'id': permission['permissions__id'],
                    }
                )
            else:
                menu_dict[permission['permissions__menu_id']] = {
                    'title': permission['permissions__menu__title'],
                    'icon': permission['permissions__menu__icon'],
                    'weight': permission['permissions__menu__weight'],
                    'children': [
                        {
                            'title': permission['permissions__title'],
                            'icon': permission['permissions__icon'],
                            'url': permission['permissions__url'],
                            'id': permission['permissions__id'],
                        }
                    ]
                }

    permission_dict = {}
    menu_list = []
    url_names = []
    for permission in permission_list:
        url_names.append(permission['permissions__url_name'])
        permission_dict[permission['permissions__id']] = permission
        if permission['permissions__menu_id']:
            menu_list.append(permission)
    # < QuerySet[{'permissions__url': '/customer/list/'}, {'permissions__url': '/customer/add/'}],
    request.session[settings.PERMISSION_KEY] = permission_dict
    request.session[settings.MENU_LIST] = menu_dict
    request.session[settings.URL_NAMES] = url_names
    # 应为将数据放入session干了两件事：
    # 1现将数据json序列化生成随机字符串
    # 2将随机字符串放入cookie中进行传输
    # 3将数据序列化之后存入数据库
    # 1在cookie中取出随机字符串
    # 2在数据库对比查找对应数据
    # 3取出对应数据解密反序列化
    # 所以要对不能序列化的数据进行转换




