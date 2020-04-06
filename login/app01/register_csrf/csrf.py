import re
from django.shortcuts import redirect,HttpResponse,render
from django.utils.deprecation import MiddlewareMixin

class User(MiddlewareMixin):
    white_list = ['/register/','/login/','/admin.*']

    def process_request(self,request):

        current_path = request.path
        for re_path in self.white_list:
            reg = r'^%s$'%re_path

            if re.search(reg,current_path):
                break
        else:
            username = request.session.get('username')
            if not username:
                return redirect('login')


        # if request.path in self.white_list:
        #     pass
        # else:
        #     is_login = request.session.get('is_login')
        #     if is_login == True:
        #         pass
        #     else:
        #         return HttpResponse('访问路径错误，请访问127.0.0.1:8000/login')