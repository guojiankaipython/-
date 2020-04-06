from django import template
from django.urls import reverse
register = template.Library()
@register.filter
def page_title(tags):
    if tags == 1:
        return '新生信息展示'
    else:
        return '学生信息'

@register.filter
def customers_swith(tags):
    if tags == 1:
        return '公户转私户'
    else:
        return '私户转公户'

@register.filter
def customers_number(request,forloop_counter):
    current_page = request.GET.get('page')

    try:
        current_page = int(current_page)
    except Exception:
        current_page = 1
    return (current_page - 1)*10 + forloop_counter

#自定义标签
@register.simple_tag
def resolve_url(request,url_name,cid):
    """

    :param request: 请求对象
    :param url_name:  url别名
    :param cid:    客户id
    :return:
    """
    from django.http.request import QueryDict
    custom_query_dict = QueryDict(mutable=True)
    custom_query_dict['next'] = request.get_full_path()   #要跳转回的url
    next_url = custom_query_dict.urlencode()    #将得到的搜索路径url编码

    reverse_url = reverse(url_name,args=(cid,))     #编辑的url    ?next=要跳转的url
    full_path = reverse_url + '?' + next_url
    return full_path

@register.filter
def contract_approved(v1):
    if v1 == True:
        return '是'
    else:
        return '否'


@register.filter
def error(v1):
    if bool(v1):
        return v1
    else:
        return ""


