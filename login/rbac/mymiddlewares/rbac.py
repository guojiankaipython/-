import re

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render,HttpResponse,redirect,reverse
from django.conf import settings

class Auth(MiddlewareMixin):

    def process_request(self,request):

        #登录认证白名单
        white_list = ['/login/','/admin/.*']
        #登录认证

        #权限认证白名单
        white_permission_list = []

        bread_crumb = [
            {'title':'首页','url':reverse('home')},
        ]
        request.pid = None



        current_path = request.path
        for i in white_list:
            if re.match(i,current_path):
                break
        else:

            is_login = request.session.get('is_login')
            if not is_login:
                return redirect('/login/')

            else:

                for purl in white_permission_list:
                    if re.match(purl,current_path):
                        return
                else:

                            #权限认证
                    permission_dict = request.session.get(settings.PERMISSION_KEY)
                    print(permission_dict)
                    for permission in permission_dict.values():
                        reg = r'^%s$'%permission['permissions__url']
                        if re.match(reg,current_path):

                            pid = permission['permissions__parent_id']
                            if pid:
                                parent_dict = permission_dict[str(pid)]

                                #添加二级菜单
                                bread_crumb.append({
                                    'title':parent_dict['permissions__title'],
                                    'url':parent_dict['permissions__url']
                                })

                                #添加子权限
                                bread_crumb.append({
                                    'title':permission['permissions__title'],
                                    'url':permission['permissions__url']
                                })


                                request.pid = pid

                            else:
                                if permission['permissions__url'] != reverse('home'):
                                    bread_crumb.append({
                                        'title':permission['permissions__title'],
                                        'url':permission['permissions__url']
                                    })
                                request.pid = permission['permissions__id']
                            request.session['bread_crumb'] = bread_crumb
                            return
                    else:
                        return HttpResponse('你不配！！！')






