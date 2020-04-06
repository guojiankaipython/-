from django import template
from django.conf import settings


register = template.Library()


@register.inclusion_tag('rbac/menu.html')
def menu(request):
    current_path = request.path
    menu_dict = request.session.get(settings.MENU_LIST)
    # for menu in menu_list:
    #     if menu['permissions__url'] == current_path:
    #         menu['class'] = 'active'
    for menu_k,menu_v in menu_dict.items():\
        
        menu_v['class'] = 'hidden'
        for path in menu_v['children']:
            path['class'] = ''
            if request.pid == path['id']:
                menu_v['class'] = ''
                path['class'] = 'active'
    menu_dict_sort = sorted(menu_dict,key=lambda x:menu_dict[x]['weight'],reverse=True)


    menu_order_dict = {}
    for i in menu_dict_sort:
        menu_order_dict[i] = menu_dict[i]
    return {'menu_order_dict':menu_order_dict}



@register.inclusion_tag('rbac/bread_crumb.html')
def bread_crumb(request):

    bread_crumb = request.session.get('bread_crumb')

    return {'bread_crumb':bread_crumb}


@register.simple_tag
def gen_role_url(request, rid):
    params = request.GET.copy()  #querydict{'uid':1,'rid':2}
    params._mutable = True
    params['rid'] = rid
    return params.urlencode()  #uid=1&rid=2